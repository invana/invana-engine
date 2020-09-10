import asyncio
import logging

import websockets

logger = logging.getLogger(__name__)

is_alive = True


async def alive():
    while is_alive:
        print('alive')
        await asyncio.sleep(300)


async def async_processing():
    print("Connecting async")
    async with websockets.connect('ws://192.168.0.10:8182/gremlin') as websocket:
        print("connected..")
        message =  b'!application/vnd.gremlin-v3.0+json{"requestId": {"@type": "g:UUID", "@value": "16f19ea9-3d61-45b5-b823-7f67199ff1b2"}, "processor": "traversal", "op": "bytecode", "args": {"gremlin": {"@type": "g:Bytecode", "@value": {"step": [["V", "98528"], ["valueMap", true]]}}, "aliases": {"g": "g"}}}'
        await websocket.send(message)
        print("Sending message")
        while True:
            try:
                message = await websocket.recv()
                print(message)

            except websockets.exceptions.ConnectionClosed:
                print('ConnectionClosed')
                is_alive = False
                break


# asyncio.get_event_loop().run_until_complete(alive())
# asyncio.get_event_loop().run_until_complete(async_processing())
asyncio.get_event_loop().run_until_complete(asyncio.wait([
   alive(),
   async_processing()
]))
