#  Copyright 2021 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging
from graphql import GraphQLSchema
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from ariadne.explorer import ExplorerGraphiQL, ExplorerApollo
from .views import HomePageView, GremlinQueryView
from ..settings import __VERSION__, __AUTHOR_NAME__, __AUTHOR_EMAIL__
from ..graphql.schema import SchemaGenerator
from ..graph import InvanaGraph
from ..graphql.graphiql.handler import make_graphiql_handler
from ..settings import GRAPH_BACKEND_CLASS, DEBUG, GRAPH_BACKEND_URL,  \
    SERVER_PORT
from .starlette import InvanaApp


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger('neo4j').setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def welcome():
    logger.info(f"""
██ ███    ██ ██    ██  █████  ███    ██  █████      ███████ ███    ██  ██████  ██ ███    ██ ███████
██ ████   ██ ██    ██ ██   ██ ████   ██ ██   ██     ██      ████   ██ ██       ██ ████   ██ ██
██ ██ ██  ██ ██    ██ ███████ ██ ██  ██ ███████     █████   ██ ██  ██ ██   ███ ██ ██ ██  ██ █████
██ ██  ██ ██  ██  ██  ██   ██ ██  ██ ██ ██   ██     ██      ██  ██ ██ ██    ██ ██ ██  ██ ██ ██
██ ██   ████   ████   ██   ██ ██   ████ ██   ██     ███████ ██   ████  ██████  ██ ██   ████ ███████
{__VERSION__} version ; {__AUTHOR_NAME__}({__AUTHOR_EMAIL__})""")
    logger.info(".................................................")
    logger.info(f"Starting Invana Engine server at 0.0.0.0:{SERVER_PORT}")
    logger.info(f"Using GRAPH_BACKEND_URL: {GRAPH_BACKEND_URL}")
    logger.info(f"Using GRAPH_BACKEND_CLASS: {GRAPH_BACKEND_CLASS}")
    logger.info(f"Using DEBUG: {DEBUG}")
    logger.info(".................................................")


welcome()

if not GRAPH_BACKEND_URL:
    logger.error(
        "ERROR: GRAPH_BACKEND_URL environment variable not set. Please fix it .")
    logger.error(
        "Exiting the program now. Please refer the documentation at https://github.com/invana/invana-engine")
    exit()


def create_app():

    routes = [
        Route('/', endpoint=HomePageView),
        WebSocketRoute( '/gremlin', GremlinQueryView),
        Mount( '/static',
            app=StaticFiles(
                packages=[
                    ('invana_engine.graphql.graphiql',
                     'static')]),
            name="static"),
    ]
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_methods=[
                "GET",
                "POST",
                "PUT",
                "DELETE"])]
    app = InvanaApp(routes=routes, middleware=middleware, debug=DEBUG)

    schema_generator = SchemaGenerator("")
    graphql_schema: GraphQLSchema = schema_generator.get_schema().graphql_schema

    # app.mount("/graph", GraphQL(schema.graphql_schema, debug=True,
    #                              websocket_handler=GraphQLTransportWSHandler(),
    #                              explorer=ExplorerGraphiQL(explorer_plugin=True ),
    #                              ))  # Graphiql IDE
    app.mount(
            "/graphql",
            GraphQL( graphql_schema,
                debug=True, explorer=ExplorerGraphiQL(),
                websocket_handler=GraphQLTransportWSHandler(),
            )
        )

    app.state.graph = InvanaGraph()
    # app.state.graph_schema = schema_generator.graph_schema
    return app


app = create_app()
