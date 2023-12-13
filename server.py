import asyncio
import websockets
import uuid

from redisqueue import Queue

worker1_queue = Queue(queue_name='worker1')

async def process(sid, result_queue, digits):
    print("Processing:", digits)

    worker1_queue.push({'sid': sid, 'digits': digits})

    return result_queue.pop()

async def accumulator(websocket, path):
    sid = str(uuid.uuid4())

    queue = Queue(queue_name=sid)
    digits = ""
    async for message in websocket:
        digits += message
        print(f"Received digit: {message}")

        if message == '0':
            result = await process(sid, queue, digits)
            await websocket.send(result)
            digits = ""  # Reset the accumulator

start_server = websockets.serve(accumulator, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
