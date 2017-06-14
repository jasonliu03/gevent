#!/usr/bin/env python
#!encoding=utf8

import os

import time
import math
import json
import webbrowser

import paste.urlparser #paste是一个WSGI工具包，在WSGI的基础上包装了几层，让应用管理和实现变得方便

import gevent
from gevent_zeromq import zmq
from geventwebsocket.handler import WebSocketHandler #基于gevent的pywsgi的WebSocket的处理程序

def main(): #主方法
    context = zmq.Context()
    gevent.spawn(zmq_server, context) #上个例子使用joinall,这个例子是spawn+start,context是参数,也就是实例化的GreenContext
    ws_server = gevent.pywsgi.WSGIServer(
        ('', 9999), WebSocketApp(context),
        handler_class=WebSocketHandler)
    http_server = gevent.pywsgi.WSGIServer(
        ('', 8000),
        paste.urlparser.StaticURLParser(os.path.dirname(__file__))) # paste.urlparser用来处理url和静态文件
    http_server.start()  #启动greenlet实例
    ws_server.start()
    webbrowser.open('http://localhost:8000/graph.html') #启动浏览器看这个页面,当正常启动后js会画图
    zmq_producer(context)

def zmq_server(context):
    sock_incoming = context.socket(zmq.SUB)
    sock_outgoing = context.socket(zmq.PUB)
    sock_incoming.bind('tcp://*:5000') #发布绑定
    sock_outgoing.bind('inproc://queue') #订阅绑定,本地(通过内存)进程（线程间）通信传输
    #sock_outgoing.bind('tcp://*:10001') 
    sock_incoming.setsockopt(zmq.SUBSCRIBE, "") #这里表示对发布的所有信息都订阅
    while True:
        msg = sock_incoming.recv()
        sock_outgoing.send(msg)

class WebSocketApp(object):

    def __init__(self, context):
        self.context = context

    def __call__(self, environ, start_response):
        ws = environ['wsgi.websocket']
        sock = self.context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "") #订阅所有信息
        sock.connect('inproc://queue') #websocket连接到订阅的地址
        #sock.connect('tcp://127.0.0.1:10001') #websocket连接到订阅的地址
        while True:
            msg = sock.recv()
            ws.send(msg)

def zmq_producer(context):  #发布的方法
    socket = context.socket(zmq.PUB)
    socket.connect('tcp://127.0.0.1:5000') #绑定到发布的socket

    while True:
        x = time.time() * 1000
        y = 2.5 * (1 + math.sin(x / 500))
        socket.send(json.dumps(dict(x=x, y=y))) #往发布socket发送数据,这样,数据会被inproc://queue订阅,而被websocket获取,根据数据展示
        gevent.sleep(0.05)

if __name__ == '__main__':
    main()
