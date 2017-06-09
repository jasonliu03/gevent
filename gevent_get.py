#!/usr/bin/env python
#!encoding=utf8

import gevent  
      
def talk(msg):  
    print(msg)  
    gevent.sleep(0)  
    print msg  
    return 100
  
g1 = gevent.spawn(talk, 'bar')  
print g1.get() # get likes join, register current greenlet to g1's notify_links
gevent.sleep(0)
#g1.join()
#gevent.core.loop().run()
#gevent.hub.get_hub().loop.run()
def f(t):  
    gevent.sleep(t)  
    return 10
      
p = gevent.spawn(f,2)  
#switcher = gevent.spawn(p.switch, "hello") #强先回调p.switch,传递参数hello, raise exception, becausenot allowed to called by other greenlets.  
result = p.get() # 2s后libev将回调f，所以p.get获取的是10   
print "result:", result
