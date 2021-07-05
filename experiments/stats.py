from invana_engine.gremlin.client import GremlinClient

gremlin_client = GremlinClient("ws://192.168.0.10:8182/gremlin")


results = gremlin_client.stats.get_vertex_stats("Planet")
print("results", results)


