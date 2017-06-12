#!/usr/bin/env python
#!encoding=utf8

import gevent
import gevent.monkey
gevent.monkey.patch_all()
import requests
from gevent.queue import Queue, Full, Empty
from gevent.pool import Pool


# if Queue() have no parameter It's unlimited
# out jd_queue just put in 100 msg.......
msg_queue = Queue(100)
jd_pool = Pool(10)
jd_msg = 1

from gevent.lock import BoundedSemaphore 
sem = BoundedSemaphore(2) # control 2 consumers

def deal_with():
    while True:
        sem.acquire()
        now_id = gevent.getcurrent()
        msg = msg_queue.get()
        gevent.sleep(5)
        print "handle " + str(msg)
        print msg_queue.qsize(), msg_queue
        sem.release()
        #print 'now start with now_id: %s' % now_id
        #print 'now end with now_id: %s' % now_id


def product_msg():
    global jd_msg
    while True:
        msg_queue.put(jd_msg)
        jd_msg += 1
        print msg_queue.qsize(), msg_queue
        gevent.sleep(0.3)


jd_pool.add(gevent.spawn(product_msg))
for i in xrange(10):
    jd_pool.add(gevent.spawn(deal_with))
jd_pool.join()
