from starlette.applications import Starlette
# from graphql.execution.executors.asyncio import AsyncioExecutor
# from graphql.execution.executors.sync import SyncExecutor
from starlette.routing import Route
from starlette.graphql import GraphQLApp
from starlette.responses import JSONResponse
from graphene import Schema
from ..gremlin import GremlinClient
import os
import time
from .schemas.query import GremlinQuery
from .schemas.mutation import GremlinMutation
gremlin_server_url = os.environ.get("GREMLIN_SERVER_URL")
shall_debug = os.environ.get("DEBUG", True)

if gremlin_server_url is None:
    raise Exception("GREMLIN_SERVER_URL environment variable not set. Please fix it.")


async def homepage(request):
    return JSONResponse({'message': 'Glad you are here, go to /graphql. Good luck with your quest.'})


routes = [
    Route('/', homepage),
    Route('/graphql', GraphQLApp(
        schema=Schema(query=GremlinQuery, mutation=GremlinMutation),
    ))
]

app = Starlette(routes=routes, debug=shall_debug)

time.sleep(1)
gremlin_client = GremlinClient(gremlin_server_url=gremlin_server_url)

app.state.gremlin_client = gremlin_client
print(".................................................")
print("Starting invana-engine server")
print(f"Using GREMLIN_SERVER_URL {gremlin_server_url}")
print(".................................................")
