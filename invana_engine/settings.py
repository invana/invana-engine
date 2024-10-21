import os

__VERSION__ = "0.0.0"
__AUTHOR_NAME__ = "Ravi Raja Merugu"
__AUTHOR_EMAIL__ = "https://github.com/rrmerugu"


GRAPH_BACKEND_URL = os.environ.get("GRAPH_BACKEND_URL", "ws://localhost:28182/gremlin")
GRAPH_BACKEND_CLASS = os.environ.get("GRAPH_BACKEND_CLASS", "invana_engine.backends.GremlinBackend")


GRAPH_BACKEND_AUTH_USERNAME = os.environ.get("GRAPH_BACKEND_AUTH_USERNAME")
GRAPH_BACKEND_AUTH_PASSWORD = os.environ.get("GRAPH_BACKEND_AUTH_PASSWORD")

# used by neo4j
GRAPH_BACKEND_DATABASE_NAME = os.environ.get("GRAPH_BACKEND_DATABASE_NAME")

# used by tinkerpop
GRAPH_BACKEND_GREMLIN_TRAVERSAL_SOURCE = os.environ.get(
    "GRAPH_BACKEND_GREMLIN_TRAVERSAL_SOURCE", "g")


DEBUG = os.environ.get("DEBUG", False)
SERVER_PORT = os.environ.get("SERVER_PORT", 8200)

DEFAULT_QUERY_TIMEOUT = 180 * 1000
DEFAULT_QUERY_PAGINATION_SIZE = 20
