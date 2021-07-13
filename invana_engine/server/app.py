#  Copyright 2020 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from ariadne import load_schema_from_path, make_executable_schema
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute, Mount
from ariadne.asgi import GraphQL, WebSocketConnectionError
from invana_engine.default_settings import GREMLIN_SERVER_SETTINGS, \
    __DEBUG__, __VERSION__
from invana_engine.server.views import HomePageView, GremlinQueryView
from invana_engine.gremlin import GremlinClient
import time
from termcolor import cprint
from invana_engine.server import mutation_type, subscription_type, query_type
import os

print(".......................................................")
cprint(f"Invana Engine Server {__VERSION__}", "cyan", attrs=["bold"])
print(".......................................................")
print(f"Using GREMLIN_SERVER_URL: {GREMLIN_SERVER_SETTINGS['gremlin_server_url']}")
print(f"Using GREMLIN_TRAVERSAL_SOURCE: {GREMLIN_SERVER_SETTINGS['traversal_source']}")
if GREMLIN_SERVER_SETTINGS['gremlin_server_username']:
    print("Using GREMLIN_SERVER_USERNAME: ******** ")
if GREMLIN_SERVER_SETTINGS['gremlin_server_password']:
    print("Using GREMLIN_SERVER_PASSWORD: ******** ")
print(f"Using DEBUG: {__DEBUG__}")
print(".......................................................")

if GREMLIN_SERVER_SETTINGS['gremlin_server_url'] is None:
    print("ERROR: GREMLIN_SERVER_URL environment variable not set. Please fix it .")
    print("Exiting the program now. Please refer the documentation at https://github.com/invanalabs/invana-engine")
    exit()

type_defs = load_schema_from_path("{}/schema/".format(os.path.dirname(os.path.abspath(__file__))))
schema = make_executable_schema(type_defs, query_type, mutation_type, subscription_type)


def on_connect(ws, payload):
    user_token = str(payload.get("authUser") or "").strip().lower()
    if "ban" in user_token:
        raise WebSocketConnectionError(
            {"message": "User is banned", "code": "BANNED", "ctx": user_token, "loc": "__ROOT__"})
    ws.scope["user_token"] = user_token or None


gremlin_client = GremlinClient(
    gremlin_server_url=GREMLIN_SERVER_SETTINGS['gremlin_server_url'],
)


def get_context(request):
    # if request.scope["type"] == "websocket":
    #     return {
    #         "user": request.scope.get("user_token"),
    #     }

    return {"request": request, "gremlin_client": gremlin_client}


routes = [
    Route('/', HomePageView),
    WebSocketRoute('/gremlin', GremlinQueryView),
    Mount('/graphql', GraphQL(schema=schema, context_value=get_context, on_connect=on_connect, debug=__DEBUG__))
]

middlewares = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=["GET", "POST", "PUT", "DELETE"])
]

app = Starlette(routes=routes, middleware=middlewares, debug=__DEBUG__)
