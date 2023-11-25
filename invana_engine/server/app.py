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
     SERVER_PORT
from invana_engine.graphql.graphiql.handler import make_graphiql_handler
# from invana_engine.graphql.schema import get_schema
from ..settings import __VERSION__, __AUTHOR_NAME__, __AUTHOR_EMAIL__
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from ariadne.asgi import GraphQL
from ..graphql.generators import SchemaGenerator
from invana_engine import InvanaGraph
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
    
        # type ShortFilm {
        #     title: String
        #     published_date: Date
        #     extended_to: [Movie!]! @relationship(label: "extended_to", direction: OUT, properties: "ExtendedAt")        
        # }

        # type Movie {
        #     title: String
        #     published_date: Date
        #     actors: [Actor!]! @relationship(label: "ACTED_IN", direction: IN, properties: "ActedIn")
        # }

        
        # type Actor {
        #     first_name: String
        #     last_name: String
        #     screen_name: String
        #     movies: [Movie!]! @relationship(label: "ACTED_IN", direction: OUT, properties: "ActedIn")
        #     shortFilms: [ShortFilm!]! @relationship(label: "ACTED_IN", direction: OUT, properties: "ActedIn")
        #     # likes: [ShortFilm!]! @relationship(label: "likes", direction: OUT, properties: "Liked")
        #     # likes2: [Movie!]! @relationship(label: "likes", direction: OUT, properties: "Liked")
        # }

        # type ActedIn @relationshipProperties {
        #     roles: [String]
        # }

        # type Liked @relationshipProperties {
        #     date: [String]
        # }

        # type ExtendedAt @relationshipProperties {
        #     date: [String]
        # }


        type Movie {
            title: String
            published_date: Date
            # actors: [Actor!]! @relationship(label: "ACTED_IN", direction: IN, properties: "ActedIn")
        }

        type ShortMovie {
            title: String
            published_date: Date
            # actors: [Actor!]! @relationship(label: "ACTED_IN", direction: IN, properties: "ActedIn")
        }

        type Actor {
            first_name: String
            last_name: String
            screen_name: String
            shortmovies: [ShortMovie!]! @relationship(label: "ACTED_IN", direction: OUT, properties: "ActedIn")
            movies: [Movie!]! @relationship(label: "ACTED_IN", direction: OUT, properties: "ActedIn")
            likess: [Movie!]! @relationship(label: "HAS_LIKED", direction: IN, properties: "Liked")
        }

        interface ActedIn @relationshipProperties {
            roles: [String]
        }

        interface Liked @relationshipProperties {
            date: Date
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