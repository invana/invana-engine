from invana_engine.gremlin.client import GremlinClient

gremlin_client = GremlinClient("ws://192.168.0.10:8182/gremlin")

results = gremlin_client.schema.get_vertex_label_schema("Teacher")
print("results", results[0])

results = gremlin_client.schema.get_graph_schema()
print("results", results[0])

results = gremlin_client.schema.get_graph_features()
print("results", results)
