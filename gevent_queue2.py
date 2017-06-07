#!/usr/bin/env python
#!encoding=utf8

import gevent
from gevent.queue import Queue
from gevent import Greenlet

class Actor(gevent.Greenlet): #自定义actor类

    def __init__(self):
        self.inbox = Queue() #收件箱作为一个队列
        Greenlet.__init__(self)

    def receive(self, message):
        raise NotImplemented() #内置常量,表面意为没有实施

    def _run(self): #
        self.running = True

        while self.running:
            message = self.inbox.get() #获取队列数据
            self.receive(message)

class Pinger(Actor):
    def receive(self, message): #重写方法
        print message
        pong.inbox.put('ping') #当获取收件箱有数据,获取数据,再放入数据(注意:是ping中放pong数据),其中pong是一个局部变量,它是Ponger的实例,以下的同理
        gevent.sleep(1)

class Ponger(Actor):
    def receive(self, message):
        print message
        ping.inbox.put('pong')
        gevent.sleep(1)

ping = Pinger()
pong = Ponger()

ping.start()
pong.start()

ping.inbox.put('start') #最开始都是阻塞的,给一个触发
gevent.joinall([ping, pong])
