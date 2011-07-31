from gevent import monkey
monkey.patch_all()

import datetime
import time
from gevent import Greenlet
from gevent import pywsgi
from gevent import queue


def current_time(body):
    current = start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=60)

    while current < end:
        current = datetime.datetime.now()
        body.put('<div>%s</div>' % current.strftime("%Y-%m-%d %I:%M:%S"))
        time.sleep(1)

    body.put('</body></html>')
    body.put(StopIteration)


def handle(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = queue.Queue()
    body.put(' ' * 1000)
    body.put("<html><body><h1>Current Time:</h1>")
    g = Greenlet.spawn(current_time, body)
    return body


server = pywsgi.WSGIServer(('127.0.0.1', 1234), handle)
print "Serving on http://127.0.0.1:1234..."
server.serve_forever()
