from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute
from starlette.graphql import GraphQLApp
from invana_engine.server.schemas.query import GremlinQuery
from .schemas.mutation import GremlinMutation
from graphene import Schema
from .views import HomePageView, GremlinQueryView
from invana_engine.gremlin import InvanaEngineClient
import time
from ..settings import gremlin_server_url, gremlin_server_password, gremlin_server_username, shall_debug, \
    gremlin_traversal_source, invana_engine_version
from termcolor import cprint

print(".......................................................")
cprint(f"Invana Engine Server {invana_engine_version}", "cyan", attrs=["bold"])
print(".......................................................")
print(f"Using GREMLIN_SERVER_URL: {gremlin_server_url}")
print(f"Using GREMLIN_TRAVERSAL_SOURCE: {gremlin_traversal_source}")
if gremlin_server_username:
    print("Using GREMLIN_SERVER_USERNAME: ******** ")
if gremlin_server_password:
    print("Using GREMLIN_SERVER_PASSWORD: ******** ")
print(f"Using DEBUG: {shall_debug}")
print(".......................................................")

if gremlin_server_url is None:
    print("ERROR: GREMLIN_SERVER_URL environment variable not set. Please fix it .")
    print("Exiting the program now. Please refer the documentation at https://github.com/invanalabs/invana-engine")
    exit()

routes = [
    Route('/', HomePageView),
    # Route('/gremlin', endpoint=query_gremlin, methods=['POST']),
    WebSocketRoute('/gremlin', GremlinQueryView),
    Route('/graphql', GraphQLApp(
        schema=Schema(query=GremlinQuery, mutation=GremlinMutation),
    ))
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=["GET", "POST", "PUT", "DELETE"])
]

app = Starlette(routes=routes, middleware=middleware, debug=shall_debug)
time.sleep(1)
gremlin_client = InvanaEngineClient(
    gremlin_server_url=gremlin_server_url,
    gremlin_server_username=gremlin_server_username,
    gremlin_server_password=gremlin_server_password,
    gremlin_traversal_source=gremlin_traversal_source
)
app.state.gremlin_client = gremlin_client
