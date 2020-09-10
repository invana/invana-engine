import asyncio
import websockets


class WebsocketHandler(object):

    def __init__(self):
        self.conn = None

    async def connect(self, url):
        print("Connecting")
        self.conn = await websockets.connect(url)
        print("Connected")

    async def send(self, msg):
        await self.conn.send(msg)

    async def recv(self):
        return await self.conn.recv()

    async def close(self):
        await self.conn.close()


async def main():
    handler = WebsocketHandler()
    await handler.connect('ws://192.168.0.10:8182/gremlin')
    message = b'!application/vnd.gremlin-v3.0+json{"requestId": {"@type": "g:UUID", "@value": "16f19ea9-3d61-45b5-b823-7f67199ff1b2"}, "processor": "traversal", "op": "bytecode", "args": {"gremlin": {"@type": "g:Bytecode", "@value": {"step": [["V", "98528"], ["valueMap", true]]}}, "aliases": {"g": "g"}}}'

    await handler.send(message)
    # await handler.send('world')
    a = await handler.recv()
    print('response is ',a)
    await handler.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
