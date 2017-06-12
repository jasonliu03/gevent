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
jd_msg = "Boom"
test_url = "http://www.baidu.com"


def deal_with():
    while True:
        try:
            now_id = gevent.getcurrent()
            msg = msg_queue.get_nowait()
            print "handle " + msg
            print 'now start with now_id: %s' % now_id
            requests.get(test_url)
            print 'now end with now_id: %s' % now_id
        except Empty:
            gevent.sleep(0)


def product_msg(jd_msg):
    while True:
        try:
            msg_queue.put_nowait(jd_msg)
            print msg_queue.qsize()
        except Full:
            gevent.sleep(5)


jd_pool.add(gevent.spawn(product_msg, jd_msg))
for i in xrange(10):
    jd_pool.add(gevent.spawn(deal_with))
jd_pool.join()
