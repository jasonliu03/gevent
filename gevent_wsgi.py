#!/usr/bin/env python
#!encoding=utf8

#from gevent.wsgi import WSGIServer
#
#def application(environ, start_response):
#    status = '200 OK'
#    body = '<p>Hello World</p>'
#
#    headers = [
#        ('Content-Type', 'text/html')
#    ]
#
#    start_response(status, headers)
#    return [body]
#
#WSGIServer(('', 10000), application).serve_forever()

#from paste import httpserver
#httpserver.serve(application, '0.0.0.0', request_queue_size=500)




from gevent.pywsgi import WSGIServer #使用pywsgi可以我们自己定义产生结果的处理引擎

def application(environ, start_response):
    status = '200 OK'

    headers = [
        ('Content-Type', 'text/html')
    ]

    start_response(status, headers)
    yield "<p>Hello" #yield出数据
    yield "World</p>"

WSGIServer(('', 10001), application).serve_forever()

#from paste import httpserver
#httpserver.serve(application, '0.0.0.0', request_queue_size=500)
