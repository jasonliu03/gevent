#!/usr/bin/env python
#!encoding=utf8

import gevent
from gevent.queue import Queue, Empty

tasks = Queue(maxsize=3)  #限制队列的长度

def worker(n):
    try:
        while True:
            task = tasks.get(timeout=1) # 减少队列,超时为1秒
            print('Worker %s got task %s' % (n, task))
            gevent.sleep(0)
    except Empty:
        print('Quitting time!')

def boss():
    """
    Boss will wait to hand out work until a individual worker is
    free since the maxsize of the task queue is 3.
    """

    for i in xrange(1,10):
        tasks.put(i)  #这里boss没有盲目的不停放入数据,而是在当最大三个队列数有空余才放入数据,事实上方法转换过程中,boss放入三个数据,worker取出三个数据,boss再放入数据....
    print('Assigned all work in iteration 1')

    for i in xrange(10,20):
        tasks.put(i)
    print('Assigned all work in iteration 2')

gevent.joinall([
    gevent.spawn(boss),
    gevent.spawn(worker, 'steve'),
    gevent.spawn(worker, 'john'),
    gevent.spawn(worker, 'bob'),
])
