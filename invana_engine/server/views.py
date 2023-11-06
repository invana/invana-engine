from starlette.responses import JSONResponse
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
import websockets
from ..settings import GRAPH_BACKEND_URL, GRAPH_BACKEND_GREMLIN_TRAVERSAL_SOURCE, \
    GRAPH_BACKEND_AUTH_USERNAME, GRAPH_BACKEND_AUTH_PASSWORD
import json
import uuid
import logging
import base64


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
        await self.gremlin.connect(GRAPH_BACKEND_URL)

    @staticmethod
    async def prepare_message(gremlin_query):
        request_id = str(uuid.uuid4())
        query_message = {
            "requestId": request_id,
            "args": {
                "gremlin": gremlin_query,
                "bindings": {},
                "language": "gremlin-groovy",
                "aliases": {"g": GRAPH_BACKEND_GREMLIN_TRAVERSAL_SOURCE},
                "session": request_id
            }
        }
        if GRAPH_BACKEND_AUTH_USERNAME or GRAPH_BACKEND_AUTH_PASSWORD:
            auth = b"".join([b"\x00", GRAPH_BACKEND_AUTH_USERNAME.encode("utf-8"),
                             b"\x00", GRAPH_BACKEND_AUTH_PASSWORD.encode("utf-8")])
            query_message['op'] = "authentication"
            query_message['processor'] = ""
            query_message['args']['sasl'] = base64.b64encode(auth).decode()
        else:
            query_message['op'] = "eval"
            query_message['processor'] = "session"
            query_message['args']['session'] = request_id
        return query_message

    async def on_receive(self, websocket, data):
        gremlin_query = data.get("gremlin")
        query_message = await self.prepare_message(gremlin_query)
        query_string = json.dumps(query_message)
        await self.gremlin.send(query_string)
        while True:
            try:
                response_data = await self.gremlin.recv()
                print(response_data)
                await websocket.send_json(json.loads(response_data))
            except websockets.exceptions.ConnectionClosed:
                logging.debug('Don\'t have any more messages. closed connection with gremlin server')
                # await self.gremlin.close()
                break

    async def on_disconnect(self, websocket, close_code):
        logging.debug("disconnected")
        await self.gremlin.close()
