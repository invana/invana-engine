import os

gremlin_server_url = os.environ.get("GREMLIN_SERVER_URL")
gremlin_server_username = os.environ.get("GREMLIN_SERVER_USERNAME")
gremlin_server_password = os.environ.get("GREMLIN_SERVER_PASSWORD")
gremlin_traversal_source = os.environ.get("GREMLIN_TRAVERSAL_SOURCE", "g")

ALLOW_FILTERING = int(os.environ.get("ALLOW_FILTERING", "0"))
IGNORE_UNINDEXED = int(os.environ.get("IGNORE_UNINDEXED", "0"))

shall_debug = os.environ.get("DEBUG", False)
server_port = os.environ.get("SERVER_PORT", 8200)
