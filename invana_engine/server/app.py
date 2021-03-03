from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
from starlette.graphql import GraphQLApp
from invana_engine.server.schemas.query import GremlinQuery
from .schemas.mutation import GremlinMutation
from graphene import Schema
from .views import homepage_view
from ..gremlin import GremlinClient
import time
from ..settings import gremlin_server_url, gremlin_server_password, gremlin_server_username, shall_debug

print(".................................................")
print("Starting Invana Engine server")
print(f"Using GREMLIN_SERVER_URL {gremlin_server_url}")
print(".................................................")

if gremlin_server_url is None:
    print("ERROR: GREMLIN_SERVER_URL environment variable not set. Please fix it .")
    print("Exiting the program now. Please refer the documentation at https://github.com/invanalabs/invana-engine")
    exit()

routes = [
    Route('/', endpoint=homepage_view),
    Route('/graphql', GraphQLApp(
        schema=Schema(query=GremlinQuery, mutation=GremlinMutation),
    ))
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=["GET", "POST", "PUT", "DELETE"])
]

app = Starlette(routes=routes, middleware=middleware, debug=shall_debug)
time.sleep(1)
gremlin_client = GremlinClient(gremlin_server_url=gremlin_server_url,
                               gremlin_server_username=gremlin_server_username,
                               gremlin_server_password=gremlin_server_password
                               )
app.state.gremlin_client = gremlin_client
