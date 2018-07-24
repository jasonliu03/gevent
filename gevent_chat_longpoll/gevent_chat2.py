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
app.config.from_object('Ttandjj.default_settings')
app.config.from_envvar('TTANDJJ_SETTINGS')

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
            time_local = time.localtime(rst[1])
            rst[1] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            rtnList.append(rst)
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

class RoomDraft(object):

    def __init__(self):
        self.users = set()
        self.draft = []
        self.redis = redis.Redis(host="localhost", port=6379)

    def backlog(self, size=1000):
        recList = self.redis.lrange("draft", 0, size)
        rtnList = []
        for e in recList:
            rst = json.loads(e)
            time_local = time.localtime(rst[1])
            rst[1] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            rtnList.append(rst)
        rtnList.reverse()
        return rtnList

    def subscribe(self, user):
        self.users.add(user)

    def add(self, message):
        self.draft.append(message)

        data = [ message, time.time() ] 
        value = json.dumps(data)
        res = self.redis.lpush("draft", value)

class User(object):

    def __init__(self):
        self.queue = queue.Queue()

rooms = {
    'LouTiKou': Room(),
    'YinShuiJi': RoomDraft(),
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

import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
# 第三方 SMTP 服务
mail_host="smtp.163.com"  #设置服务器
mail_user="ziqidonglai03@163.com"    #用户名
mail_pass = app.config['PASSWORD']
 
 
sender = 'ziqidonglai03@163.com'
receivers = ['ziqidonglai03@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
@app.route('/<room>/<uid>') #请求被转到了这里
def join(room, uid):
    user = users.get(uid, None)
    if uid != "TTLove222" and uid != "JJLove526":
        return "Please Check your Name, My love ..."

    if not user:
        users[uid] = user = User()

    if uid == "TTLove222": 
        try:
            smtpObj = smtplib.SMTP() 
            smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
            smtpObj.starttls()
            smtpObj.login(mail_user,mail_pass)  

            time_local = time.localtime(time.time())
            strTime = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            message = MIMEText('ID: 222 ' + 'time:' + strTime, 'plain', 'utf-8')
            message['From'] = Header("vivian@163.com", 'utf-8')
            message['To'] =  Header("ziqidonglai03@163.com", 'utf-8')
             
            subject = 'ttandjj'
            message['Subject'] = Header(subject, 'utf-8')
            smtpObj.sendmail(sender, receivers, message.as_string())
            print "邮件发送成功"
        except smtplib.SMTPException as e:
            print e 
            print "Error: 无法发送邮件"

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

@app.route("/putdraft/yinshuiji/<uid>", methods=["POST"]) #通过这个url
def putmsg(uid):
    user = users[uid]
    room = rooms['YinShuiJi']

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


