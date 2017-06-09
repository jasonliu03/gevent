#!/usr/bin/env python
#!encoding=utf8
import gevent

def f(source):  
    print source.value  
gevent.spawn(lambda: 'gg').link(f)  
gevent.sleep(1) 

from gevent.event import AsyncResult  
a = AsyncResult()  
gevent.spawn(lambda: 'gg2').link(a)  
print a.get()  
gevent.sleep(1)

