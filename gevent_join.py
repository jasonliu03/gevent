#!/usr/bin/env python
#!encoding=utf8

import gevent  
      
def talk(msg):  
    print(msg)  
    gevent.sleep(0)  
    print msg  
  
g1 = gevent.spawn(talk, 'bar')  
#gevent.sleep(0)
#g1.join()
#gevent.core.loop().run()
gevent.hub.get_hub().loop.run()
