from starlette.applications import Starlette
# from graphql.execution.executors.asyncio import AsyncioExecutor
# from graphql.execution.executors.sync import SyncExecutor
from starlette.routing import Route
from starlette.graphql import GraphQLApp
from graphene import Schema
from .gql import GremlinQuery
from ..gremlin import GremlinClient
import os
import time

gremlin_server_url = os.environ.get("GREMLIN_SERVER_URL")



if gremlin_server_url is None:
    raise Exception("GREMLIN_SERVER_URL environment variable not set. Please fix it.")


routes = [
    Route('/', GraphQLApp(
        schema=Schema(query=GremlinQuery),
    ))
]

app = Starlette(routes=routes)

time.sleep(1)
gremlin_client = GremlinClient(
    gremlin_server_url=gremlin_server_url
)

app.state.gremlin_client = gremlin_client
print(".................................................")
print("Starting invana-engine server")
print(f"Using GREMLIN_SERVER_URL {gremlin_server_url}")
print(".................................................")
