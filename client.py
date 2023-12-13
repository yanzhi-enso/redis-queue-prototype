import asyncio
import websockets
import random

async def send_random_digits(uri):
    async with websockets.connect(uri) as websocket:
        last_digit = None
        digit_count = 0

        while True:
            # If 10 digits have been sent without a 0, force a 0
            if digit_count >= 10:
                digit = 0
                digit_count = 0
            else:
                # Generate a random digit different from the last one
                digit = random.choice([d for d in range(1, 6) if d != last_digit])
                digit_count += 1

            last_digit = digit

            print("Sending digit:", digit)
            await websocket.send(str(digit))

            # Wait for the response if the digit is 0
            if digit == 0:
                response = await websocket.recv()
                print("Received processed number:", response)
                digit_count = 0  # Reset the digit count

            # Pause for 5 seconds if digit is 0, otherwise 0.5 seconds
            await asyncio.sleep(5 if digit == 0 else 0.5)

asyncio.get_event_loop().run_until_complete(send_random_digits('ws://localhost:8765'))
