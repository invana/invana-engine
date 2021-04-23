from starlette.responses import JSONResponse
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
import websockets
from ..settings import gremlin_server_url, gremlin_traversal_source
import json
import uuid
import logging


class GremlinWebsocketHandler(object):
    conn = None

    async def connect(self, url):
        self.conn = await websockets.connect(url)

    async def send(self, msg):
        await self.conn.send(msg)

    async def recv(self):
        return await self.conn.recv()

    async def close(self):
        await self.conn.close()


class HomePageView(HTTPEndpoint):

    async def get(self, request):
        return JSONResponse({'message': 'Hello world! go to /graphql'})


class GremlinQueryView(WebSocketEndpoint):
    encoding = 'json'
    gremlin = GremlinWebsocketHandler()

    async def on_connect(self, websocket):
        logging.debug("connected")
        await websocket.accept()
        await self.gremlin.connect(gremlin_server_url)

    async def on_receive(self, websocket, data):
        request_id = str(uuid.uuid4())
        query_message = {
            # "requestId": {"@type": "g:UUID", "@value": str(uuid.uuid4())},
            "requestId": request_id,
            "op": "eval",
            "processor": "session",
            "args": {
                "gremlin": data.get("gremlin"),
                "bindings": {},
                "language": "gremlin-groovy",
                "aliases": {"g": gremlin_traversal_source},
                "session": request_id
            }
        }
        query_string = json.dumps(query_message)
        await self.gremlin.send(query_string)
        while True:
            try:
                response_data = await self.gremlin.recv()
                await websocket.send_json(json.loads(response_data))
            except websockets.exceptions.ConnectionClosed:
                logging.debug('Don\'t have any more messages. closed connection with gremlin server')
                # await self.gremlin.close()
                break

    async def on_disconnect(self, websocket, close_code):
        logging.debug("disconnected")
        await self.gremlin.close()
