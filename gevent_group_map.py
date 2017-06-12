#!/usr/bin/env python
#!encoding=utf8

import gevent
from gevent.pool import Group

def intensive(n):
    gevent.sleep(3 - n)
    return 'task', n

print('Ordered')
ogroup = Group()
x = ogroup.imap(intensive, xrange(3))
print x

for x in ogroup.imap(intensive, xrange(3)):
    print x
                


import gevent
from gevent.pool import Group

def intensive(n):
    gevent.sleep(3 - n)
    return 'task', n


igroup = Group()
for i in igroup.imap_unordered(intensive, xrange(3)):
    print(i)
