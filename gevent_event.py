#!/usr/bin/env python

import gevent
from gevent.event import AsyncResult
a = AsyncResult()

def setter():
    gevent.sleep(3)
    a.set('Hello!') # a value or an exception instance

def waiter():
    print a.get() # return the value or the exception

gevent.joinall([
    gevent.spawn(setter),
    gevent.spawn(waiter),
])
