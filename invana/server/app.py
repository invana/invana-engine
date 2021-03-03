from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
# from graphql.execution.executors.asyncio import AsyncioExecutor
# from graphql.execution.executors.sync import SyncExecutor
from starlette.routing import Route, Mount
from starlette.graphql import GraphQLApp
from invana.server.schemas.query import GremlinQuery
from .schemas.mutation import GremlinMutation
from graphene import Schema
from .views import homepage_view
from ..gremlin import GremlinClient
import os
import time

gremlin_server_url = os.environ.get("GREMLIN_SERVER_URL")
gremlin_server_username = os.environ.get("GREMLIN_SERVER_USERNAME")
gremlin_server_password = os.environ.get("GREMLIN_SERVER_PASSWORD")
shall_debug = os.environ.get("DEBUG", True)
print(".................................................")
print("Starting invana-engine server")
print(f"Using GREMLIN_SERVER_URL {gremlin_server_url}")
print(".................................................")

if gremlin_server_url is None:
    raise Exception("GREMLIN_SERVER_URL environment variable not set. Please fix it.")

routes = [
    Route('/', endpoint=homepage_view),
    Route('/graphql', GraphQLApp(
        schema=Schema(query=GremlinQuery, mutation=GremlinMutation),
    )),

]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'],
               allow_methods=["GET", "POST", "PUT", "DELETE"])
]

app = Starlette(routes=routes, middleware=middleware, debug=shall_debug)

time.sleep(1)
gremlin_client = GremlinClient(gremlin_server_url=gremlin_server_url,
                               gremlin_server_username=gremlin_server_username,
                               gremlin_server_password=gremlin_server_password
                               )
app.state.gremlin_client = gremlin_client
