from invana_engine.gremlin.client import GremlinClient

gremlin_client = GremlinClient("ws://192.168.0.10:8182/gremlin")

results = gremlin_client.schema.get_all_vertices_schema()
print("results", results)

# results = gremlin_client.schema.get_all_edges_schema()
# print("results", results)

results = gremlin_client.schema.get_vertex_schema(results[0]['label'])
print("results", results)

exit()

results = gremlin_client.schema.get_vertex_label_schema("Teacher")
print("results", results[0])

results = gremlin_client.schema.get_graph_schema()
print("results", results[0])

results = gremlin_client.schema.get_graph_features()
print("results", results)


results = gremlin_client.query("""
mgmt = graph.openManagement()


person = mgmt.makeVertexLabel('person').make()
name = mgmt.makePropertyKey('name').dataType(String.class).cardinality(Cardinality.SET).make()
birthDate = mgmt.makePropertyKey('birthDate').dataType(Long.class).cardinality(Cardinality.SINGLE).make()
mgmt.addProperties(person, name, birthDate)


follow = mgmt.makeEdgeLabel('follow').multiplicity(MULTI).make()
name = mgmt.makePropertyKey('name').dataType(String.class).cardinality(Cardinality.SET).make()
mgmt.addProperties(follow, name)
mgmt.commit()
""")

print("results", results)
