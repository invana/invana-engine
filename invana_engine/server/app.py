from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute, Mount
# from starlette.graphql import GraphQLApp
from invana_engine.server.schemas import QuerySchema, SubscriptionSchema
from invana_engine.default_settings import GREMLIN_SERVER_SETTINGS, \
    __DEBUG__, __VERSION__
from invana_engine.server.views import HomePageView, GremlinQueryView
from graphene import Schema
from invana_engine.gremlin import GremlinClient
import time
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler

# from invana_engine.server.schemas.query import GremlinQuery
# from .schemas.mutation import GremlinMutation
# from graphene import Schema
# from .views import HomePageView, GremlinQueryView
# from invana_engine.gremlin import InvanaEngineClient
# import time
# from ..settings import gremlin_server_url, gremlin_server_password, gremlin_server_username, shall_debug, \
#     gremlin_traversal_source, __VERSION__
from termcolor import cprint

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

schema = Schema(query=QuerySchema, subscription=SubscriptionSchema)

routes = [
    Route('/', HomePageView),
    # Route('/gremlin', endpoint=query_gremlin, methods=['POST']),
    WebSocketRoute('/gremlin', GremlinQueryView),
    Mount('/graphql', GraphQLApp(schema=schema,  on_get=make_playground_handler()))
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=["GET", "POST", "PUT", "DELETE"])
]

app = Starlette(routes=routes, middleware=middleware, debug=__DEBUG__)
time.sleep(1)
gremlin_client = GremlinClient(
    gremlin_server_url=GREMLIN_SERVER_SETTINGS['gremlin_server_url'],
)
app.state.gremlin_client = gremlin_client
