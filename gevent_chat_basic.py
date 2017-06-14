#!/usr/bin/env python
#!encoding=utf8

import gevent
from gevent.queue import Queue
from gevent.server import StreamServer

users = {}  # mapping of username -> Queue


def broadcast(msg):
    msg += '\n'
    for v in users.values():
        v.send(msg)

def read_name(f, sock):
    while True:
        sock.sendall('Please enter your name: ')
        name = f.readline().strip()
        if name:
            if name in users:
                sock.sendall('That username is already taken.\n')
            else:
                return name


def handle(sock, client_addr):
    f = sock.makefile()

    name = read_name(f, sock)

    broadcast('## %s joined from %s.' % (name, client_addr[0]))

    users[name] = sock

    try:
        while(1):
            msg = sock.recv(1024)
            if msg:
                broadcast(msg)
            else:
                break
    finally:
        del(users[name])
        broadcast('## %s left the chat.' % name)


if __name__ == '__main__':
    import sys
    try:
        myip = sys.argv[1]
    except IndexError:
        myip = '0.0.0.0'

    print 'To join, telnet %s 10000' % myip
    s = StreamServer((myip, 10000), handle)
    s.serve_forever()
