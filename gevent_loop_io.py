#!/usr/bin/env python
#!encoding=utf8

import socket  # 普通socket
import gevent  
from gevent.core import loop  

def handler(s, cio):
    msg = s.recv(100)
    if not msg:
        print "left:", s.getpeername()
        cio.stop()
        s.close()
    else:
        s.send("%s\r\n" %msg)  

  
def f():  
    s, address = sock.accept()  
    print "join:", address  
    cio = loop.io(s.fileno(),1)
    cio.start(handler, s, cio)


loop = loop()  
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
sock.bind(("localhost",10000))  
sock.listen(10)  
io = loop.io(sock.fileno(),1) #1代表read  
io.start(f)  
loop.run()  
