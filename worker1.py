from redisqueue import Queue

worker1_queue = Queue(queue_name='worker1')

encoder = {
    '0': '\n',
    '1': 'a',
    '2': 'b',
    '3': 'c',
    '4': 'd',
    '5': 'e',
    '6': 'f',
}

while True:
    message = worker1_queue.pop()
    print("received a task, processing")

    digits = message['digits']
    sid = message['sid']

    res = [encoder[d] for d in digits]

    queue = Queue(queue_name=sid)
    queue.push(res)