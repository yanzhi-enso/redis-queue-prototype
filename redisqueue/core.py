import redis
import json

class Queue:
    def __init__(self, host='localhost', port=6379, db=0, queue_name='myqueue'):
        """
        Initialize a Redis connection and specify the queue name.
        """
        self.r = redis.Redis(host=host, port=port, db=db)
        self.queue_name = queue_name

    def push(self, task):
        """
        Push a task to the Redis queue. The task should be a JSON object with 'sid' and 'data'.
        """
        task_json = json.dumps(task)
        self.r.lpush(self.queue_name, task_json)

    def pop(self):
        """
        Pop a task from the Redis queue. Returns a task as a JSON object.
        """
        _, task_json = self.r.brpop(self.queue_name)
        return json.loads(task_json)

if __name__ == "__main__":
    # Example Usage
    queue = Queue(queue_name='myworkerqueue')
    queue.push({'sid': '123', 'data': 'Example Task'})

    task = queue.pop()
    print(task)  # Output: {'sid': '123', 'data': 'Example Task'}
