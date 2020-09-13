# from gremlin_python.driver.tornado.transport import TornadoTransport
# import asyncio
# import websockets
#
#
# class CustomTornadoTransport(TornadoTransport):
#
#     def __init__(self):
#         self._loop = asyncio.new_event_loop()
#
#     def connect(self, url, headers=None):
#         self._ws = self._loop.run_until_complete(
#             websockets.connect(url)
#         )
#
#     def write(self, message):
#         self._loop.run_until_complete(self._ws.send(message))
#
#     def read(self):
#         _ = self._loop.run_until_complete(self._ws.recv())
#         return _
#
#     def close(self):
#         self._ws.close()
#         self._loop.close()
#
#     def closed(self):
#         return not self._ws.protocol
