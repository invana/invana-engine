from starlette.applications import Starlette
# from graphql.execution.executors.asyncio import AsyncioExecutor
# from graphql.execution.executors.sync import SyncExecutor
from starlette.routing import Route
from starlette.graphql import GraphQLApp
from invana.server.schemas.query import GremlinQuery
from .schemas.mutation import GremlinMutation
from starlette.responses import JSONResponse
from graphene import Schema
from ..gremlin import GremlinClient
import os
import time

gremlin_server_url = os.environ.get("GREMLIN_SERVER_URL")
shall_debug = os.environ.get("DEBUG", True)

if gremlin_server_url is None:
    raise Exception("GREMLIN_SERVER_URL environment variable not set. Please fix it.")


async def gremlin_query(request):
    payload = await request.json()
    if "gremlin" not in payload:
        return JSONResponse({"message": "Invalid payload! Query should have key 'gremlin'"})
    print("=====request.app.state.gremlin_client", request.app.state.gremlin_client)
    data = request.app.state.gremlin_client.execute_query(payload['gremlin'])
    return JSONResponse({'message': 'Query successful', 'data': data})


async def homepage(request):
    return JSONResponse({'message': 'Hello world! go to /graphql'})


routes = [
    Route('/', homepage),
    Route('/graphql', GraphQLApp(
        schema=Schema(query=GremlinQuery, mutation=GremlinMutation),
    )),
    Route('/gremlin', gremlin_query, methods=["POST"])

]

app = Starlette(routes=routes, debug=shall_debug)

time.sleep(1)
gremlin_client = GremlinClient(gremlin_server_url=gremlin_server_url)
app.state.gremlin_client = gremlin_client
print(".................................................")
print("Starting invana-engine server")
print(f"Using GREMLIN_SERVER_URL {gremlin_server_url}")
print(".................................................")
