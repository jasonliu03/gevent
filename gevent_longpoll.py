#!/usr/bin/env python
#!encoding=utf8

import gevent
from gevent.queue import Queue, Empty
from gevent.pywsgi import WSGIServer
import json

data_source = Queue()

def producer():
    while True:
        data_source.put_nowait('Hello World') #往队列非阻塞的放入数据
        gevent.sleep(3)

def ajax_endpoint(environ, start_response):
    print "current:", gevent.getcurrent()
    status = '200 OK'
    headers = [
        ('Content-Type', 'application/json') #设定网络文件的类型是json
    ]
    try:
        datum = data_source.get(timeout=1)
    except Empty:
        datum = [] #假如gevent.sleep的时间设置的长一些(比如5s),在不停刷新过程中会获得空列表

    start_response(status, headers)
    return json.dumps(datum) #返回数据,打印出来的数据是一个带引号的字符串

gevent.spawn(producer)

WSGIServer(('', 10000), ajax_endpoint).serve_forever()
