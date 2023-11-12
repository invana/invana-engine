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
from starlette.applications import Starlette
import logging
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute
from .views import HomePageView, GremlinQueryView
from invana_engine.settings import GRAPH_BACKEND, DEBUG, GRAPH_BACKEND_URL,  \
    GRAPH_BACKEND_GREMLIN_TRAVERSAL_SOURCE, SERVER_PORT
from starlette_graphene3 import GraphQLApp
from invana_engine.graphql.graphiql.handler import make_graphiql_handler
# from invana_engine.graphql.schema import get_schema
from ..settings import __VERSION__, __AUTHOR_NAME__, __AUTHOR_EMAIL__
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from ariadne.asgi import GraphQL
# from ..graphql.generators.ariadne_generator import  \
#     AriadneGraphQLSchemaGenerator, generate_schema_dynamically
from ..graphql.generators import SchemaGenerator
# from ..graphql.generators.schema_generator_examples import example_schema_with_subscription, example_schema
from invana_engine.connector.graph import InvanaGraph
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from ariadne.explorer import ExplorerGraphiQL, ExplorerApollo
import logging


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
    logger.info(f"Using GRAPH_BACKEND: {GRAPH_BACKEND}")
    logger.info(f"Using DEBUG: {DEBUG}")
    logger.info(".................................................")


welcome()

if GRAPH_BACKEND_URL is None:
    logger.error("ERROR: GRAPH_BACKEND_URL environment variable not set. Please fix it .")
    logger.error(
        "Exiting the program now. Please refer the documentation at https://github.com/invana/invana-engine")
    exit()


def create_app():


    schema_def =  """

        type Person {
            id: ID!
            email: String!
            first_name: String
            projects: [Project!]! @relationship(label: "authored_project", direction: OUT)
        }

        type Project {
            id: ID!
            name: String!
            description: String
        }
"""

    routes = [
        Route('/', endpoint=HomePageView),
        WebSocketRoute('/gremlin', GremlinQueryView),
        Mount('/static', app=StaticFiles(packages=[('invana_engine.graphql.graphiql', 'static')]), name="static"),
    ]
    middleware = [
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=["GET", "POST", "PUT", "DELETE"])
    ]
    app = Starlette(routes=routes, middleware=middleware, debug=DEBUG)

    # schema = example_schema_with_subscription()
    # schema = example_schema()
    # schema = generate_schema_dynamically()

    schema =  SchemaGenerator(schema_def).get_schema() 
    schema = schema.graphql_schema
    # app.mount("/graph", GraphQL(schema.graphql_schema, debug=True,
    #                              websocket_handler=GraphQLTransportWSHandler(),
    #                              explorer=ExplorerGraphiQL(explorer_plugin=True ), 
    #                              ))  # Graphiql IDE
    app.mount("/graph", GraphQL(schema, debug=True,
                                explorer=ExplorerApollo( ), 
                                websocket_handler=GraphQLTransportWSHandler(),
                            )) 

    app.state.graph = InvanaGraph()
    return app


app = create_app()