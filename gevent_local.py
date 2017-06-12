#!/usr/bin/env python
#!encoding=utf8

import gevent
from gevent.local import local


class MyLocal(local):
    __slots__ = ('number', 'x')

    # number = 2
    initialized = False

    def __init__(self, **kw):
        if self.initialized:
            raise SystemError('__init__ called too many times')
        self.initialized = True
        self.__dict__.update(kw)

    def squared(self):
        return self.number ** 2

stash = MyLocal()

def f1():
    stash.x = 1
    stash.number = 3
    print stash.x
    print stash.number

def f2():
    stash.y = 2
    print(stash.y)

    try:
        print stash.x # can access var from g1
        print stash.number
    except AttributeError:
        print("x is not local to f2")

g1 = gevent.spawn(f1)
g2 = gevent.spawn(f2)

gevent.joinall([g1, g2])
