import asyncio
import websockets


class WebsocketHandler(object):

    def __init__(self):
        self.conn = None
        self._loop = asyncio.get_event_loop()

    def connect(self, url):
        print("Connecting")
        self.conn = self._loop.run_until_complete(
            websockets.connect(url)
        )
        print("Connected")

    def send(self, msg):
        return self._loop.run_until_complete(

            self.conn.send(msg)

        )

    def recv(self):
        return self._loop.run_until_complete(
            # asyncio.wait[
            self.conn.recv()
            # ]
        )

    def close(self):
        self._loop.run_until_complete(
            self.conn.close()

        )


def main():
    handler = WebsocketHandler()
    handler.connect('ws://192.168.0.10:8182/gremlin')
    message = b'!application/vnd.gremlin-v3.0+json{"requestId": {"@type": "g:UUID", "@value": "16f19ea9-3d61-45b5-b823-7f67199ff1b2"}, "processor": "traversal", "op": "bytecode", "args": {"gremlin": {"@type": "g:Bytecode", "@value": {"step": [["V", "98528"], ["valueMap", true]]}}, "aliases": {"g": "g"}}}'

    handler.send(message)
    # await handler.send('world')
    a = handler.recv()
    print('response is ', a)
    handler.close()


if __name__ == '__main__':
    main()
