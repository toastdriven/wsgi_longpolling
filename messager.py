import redis

server = redis.Redis(host='localhost', port=6379, db=0)

while True:
    message = raw_input("What to say: ")
    server.publish('messages', message)

    if message == 'quit':
        break
