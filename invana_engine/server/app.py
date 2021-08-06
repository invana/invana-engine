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
from ariadne.asgi import GraphQL
from invana_engine.default_settings import GREMLIN_SERVER_SETTINGS, \
    __DEBUG__, __VERSION__
from invana_engine.server.views import HomePageView, GremlinQueryView
from invana_py import GremlinClient
import time
from termcolor import cprint
# from invana_engine.server.pubsub import pubsub
from invana_engine.server.resolvers import query_type
import os
import warnings

print(".......................................................")
cprint(f"Invana Engine Server {__VERSION__}", "cyan", attrs=["bold"])
print(".......................................................")
print(f"Using GREMLIN_SERVER_URL: {GREMLIN_SERVER_SETTINGS['gremlin_server_url']}")
print(f"Using GREMLIN_TRAVERSAL_SOURCE: {GREMLIN_SERVER_SETTINGS['traversal_source']}")
if GREMLIN_SERVER_SETTINGS['gremlin_server_username']:
    print("Using GREMLIN_SERVER_USERNAME: ******** ")
if GREMLIN_SERVER_SETTINGS['gremlin_server_password']:
    print("Using GREMLIN_SERVER_PASSWORD: ******** ")

print(f"Using ALLOW_FILTERING: {GREMLIN_SERVER_SETTINGS['ALLOW_FILTERING']}")
if GREMLIN_SERVER_SETTINGS['ALLOW_FILTERING'] == 1:
    warnings.warn("Allowing filtering without labels. This may have performance implications in production. ")
print(f"Using IGNORE_UNINDEXED: {GREMLIN_SERVER_SETTINGS['IGNORE_UNINDEXED']}")
if GREMLIN_SERVER_SETTINGS['IGNORE_UNINDEXED'] == 1:
    warnings.warn("Allowing unindexed traversal. This may have performance implications in production.")

print(f"Using DEBUG: {__DEBUG__}")
print(".......................................................")

if GREMLIN_SERVER_SETTINGS['gremlin_server_url'] is None:
    print("ERROR: GREMLIN_SERVER_URL environment variable not set. Please fix it .")
    print("Exiting the program now. Please refer the documentation at https://github.com/invanalabs/invana-engine")
    exit()

type_defs = load_schema_from_path("{}/schema/".format(os.path.dirname(os.path.abspath(__file__))))
schema = make_executable_schema(type_defs, query_type)


# def on_connect(ws, payload):
#     user_token = str(payload.get("authUser") or "").strip().lower()
#     if "ban" in user_token:
#         raise WebSocketConnectionError(
#             {"message": "User is banned", "code": "BANNED", "ctx": user_token, "loc": "__ROOT__"})
#     ws.scope["user_token"] = user_token or None
#


def get_context(request):
    # if request.scope["type"] == "websocket":
    #     return {
    #         "user": request.scope.get("user_token"),
    #     }

    return {"request": request, "gremlin_client": GremlinClient(
        GREMLIN_SERVER_SETTINGS['gremlin_server_url'],
        traversal_source=GREMLIN_SERVER_SETTINGS['traversal_source'],
        username=GREMLIN_SERVER_SETTINGS['gremlin_server_username'],
        password=GREMLIN_SERVER_SETTINGS['gremlin_server_password'],
    ),
            # "pubsub": pubsub
            }


routes = [
    Route('/', HomePageView),
    WebSocketRoute('/gremlin', GremlinQueryView),
    Mount('/graphql', GraphQL(schema=schema,
                              context_value=get_context,
                              # on_connect=on_connect,
                              debug=__DEBUG__))
]

middlewares = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=["GET", "POST", "PUT", "DELETE"])
]

app = Starlette(
    routes=routes, middleware=middlewares,
    debug=__DEBUG__,
    # on_startup=[pubsub.connect],
    # on_shutdown=[pubsub.disconnect],
)
