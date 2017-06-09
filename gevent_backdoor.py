#!/usr/bin/env python
#!encoding=utf8

from gevent.backdoor import BackdoorServer  
BackdoorServer(('127.0.0.1', 9000)).serve_forever()  
