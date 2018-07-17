#!/usr/bin/env python
#!encoding=utf8

from gevent import monkey

monkey.patch_all() #给模块打包
from flask import Flask, render_template, request, json #也可以用其它比如django.tornado,bottle等

from gevent import queue
from gevent.pywsgi import WSGIServer
import redis
import json
import time

app = Flask(__name__)
app.debug = True

class Room(object):

    def __init__(self):
        self.users = set()
        self.messages = []
        self.redis = redis.Redis(host="localhost", port=6379)

    def backlog(self, size=100):
        recList = self.redis.lrange("messages", 0, size)
        rtnList = []
        for e in recList:
            rst = json.loads(e)
            rtnList.append(rst[0])
        rtnList.reverse()
        return rtnList

    def subscribe(self, user):
        self.users.add(user)

    def add(self, message):
        for user in self.users:
            user.queue.put_nowait(message)
        self.messages.append(message)

        data = [ message, time.time() ] 
        value = json.dumps(data)
        res = self.redis.lpush("messages", value)

class User(object):

    def __init__(self):
        self.queue = queue.Queue()

rooms = {
    'LouTiKou': Room(),
    'YinShuiJi': Room(),
}

users = {}

@app.route('/') #flask指定url的处理使用路由的方式,访问页面地址根目录就会执行choose_name
def choose_name():
    return render_template('choose.html') #然后调用模板choose.html,这个html文件最后使用了GET方法提交了一个uid页面(/<uid>)

@app.route('/<uid>') #请求被转到了这里
def main(uid):
    return render_template('main.html', #调用模板提供几个room的连接
        uid=uid,
        rooms=rooms.keys() #格局选择的连接,通过GET方法转到那个相应url:/<room>/<uid>
    )

@app.route('/<room>/<uid>') #请求被转到了这里
def join(room, uid):
    user = users.get(uid, None)

    if not user:
        users[uid] = user = User()

    active_room = rooms[room]
    active_room.subscribe(user)
    print 'subscribe', active_room, user

    messages = active_room.backlog()

    return render_template('room.html', #room.html包含一个POST提交方式,把你的聊天数据提交,并且更新页面(通过jquery的ajax调用url/poll/<uid>)
        room=room, uid=uid, messages=messages)

@app.route("/put/<room>/<uid>", methods=["POST"]) #通过这个url
def put(room, uid):
    user = users[uid]
    room = rooms[room]

    message = request.form['message']
    room.add(': '.join([uid, message]))

    return ''

@app.route("/poll/<uid>", methods=["POST"])
def poll(uid):
    try:
        msg = users[uid].queue.get(timeout=10)
    except queue.Empty:
        msg = []
    return json.dumps(msg) #返回队列中包含的聊天记录

if __name__ == "__main__":
    http = WSGIServer(('', 10000), app)
    http.serve_forever()


