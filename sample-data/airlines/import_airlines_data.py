"""
This script will import airlines data from Kevin Lawrence's book
https://github.com/krlawrence/graph/tree/master/sample-data

"""

from invana_engine.gremlin.client import GremlinClient

graph_client = GremlinClient(gremlin_server_url="ws://127.0.0.1:8182/gremlin")
