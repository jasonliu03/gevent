#!/usr/bin/env python

##############sync, async#############

import gevent
import random
import time

def task_block(pid):
    etime = random.randint(0,5)*0.01
    gevent.sleep(etime)
    print('Task_blcok', pid, 'done:%s' % etime)

def task_nonblock(pid):
    print('Task_nonblock', pid, 'done')

def synchronous():  
    for i in range(1,10):
        task_block(i)

def synchronous2(): 
    threads = [gevent.spawn(task_nonblock, i) for i in xrange(10)]
    gevent.joinall(threads)

def asynchronous(): 
    threads = [gevent.spawn(task_block, i) for i in xrange(10)]
    gevent.joinall(threads)

################ thread with block ##################
print('Synchronous:')
time_start = time.time()
synchronous()
etime_sum = time.time() - time_start
print('synchronous etime sum:%s' % etime_sum) # etime_sum == the sum time

################ coroutine without block ##################
print('Synchronous2:')
time_start = time.time()
synchronous2()
etime_sum = time.time() - time_start
print('synchronous2 etime sum:%s' % etime_sum) # etime_sum == the sum time

################ coroutine with block ##################
print('Asynchronous:')
time_start = time.time()
asynchronous()
etime_sum = time.time() - time_start
print('Asynchronous etime sum:%s' % etime_sum) # etime_sum == the longest time
