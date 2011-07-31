from gevent import monkey
monkey.patch_all()

import time
from gevent import Greenlet
from gevent import pywsgi
from gevent import queue
import redis


def process_messages(body):
    server = redis.Redis(host='localhost', port=6379, db=0)
    client = server.pubsub()
    client.subscribe('messages')

    while True:
        message = client.listen().next()
        print "Saw: %s" % message['data']

        if message['data'] == 'quit':
            body.put("Server closed.")
            body.put(StopIteration)

        body.put("<div>%s</div>\n" % message['data'])
        time.sleep(1)


def handle(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = queue.Queue()
    body.put(' ' * 1000)
    body.put("<html><body><h1>Messages:</h1>")
    g = Greenlet.spawn(process_messages, body)
    return body


server = pywsgi.WSGIServer(('127.0.0.1', 1234), handle)
print "Serving on http://127.0.0.1:1234..."
server.serve_forever()
