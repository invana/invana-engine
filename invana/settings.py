import os

gremlin_server_url = os.environ.get("GREMLIN_SERVER_URL")
gremlin_server_username = os.environ.get("GREMLIN_SERVER_USERNAME")
gremlin_server_password = os.environ.get("GREMLIN_SERVER_PASSWORD")
shall_debug = os.environ.get("DEBUG", False)
server_port = os.environ.get("SERVER_PORT", 8200)
