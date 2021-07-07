from invana_engine.gremlin.client import GremlinClient

gremlin_client = GremlinClient("ws://192.168.0.10:8182/gremlin")

results = gremlin_client.schema.get_graph_schema()
print("results", results)
exit()
results = gremlin_client.schema.create_vertex_label_with_schema(
    "my_vertex_6",
    name6={"data_type": "String", "cardinality_type": "SINGLE"},
    age6={"data_type": "Integer", "cardinality_type": "SINGLE"},
)
print("results", results)

results = gremlin_client.schema.create_edge_label_with_schema(
    "my_edge_5",
    name5={"data_type": "String", "cardinality_type": "SINGLE"},
    age5={"data_type": "Integer", "cardinality_type": "SINGLE"},
)
print("results", results)

# results = gremlin_client.query(
# """
# mgmt = graph.openManagement()
#
# planet = mgmt.makeVertexLabel('Planet4').make()
# name3 = mgmt.makePropertyKey('name4').dataType(String.class).cardinality(org.janusgraph.core.Cardinality.SET).make()
# birthDate3 = mgmt.makePropertyKey('birthDate4').dataType(Long.class).cardinality(org.janusgraph.core.Cardinality.SINGLE).make()
# mgmt.addProperties(planet, name3, birthDate3)
# mgmt.commit()
#
# """
# )
# print("results", results)
#


results = gremlin_client.schema.get_graph_schema()
print("results", results)

# results = gremlin_client.schema.get_all_vertices_schema()
# print("results", results)
# #
# results = gremlin_client.schema.get_all_edges_schema()
# print("results", results)
#
# results = gremlin_client.schema.get_vertex_schema(results[0]['label'])
# print("results", results)
#
# exit()
#
# results = gremlin_client.schema.get_vertex_label_schema("Teacher")
# print("results", results[0])

results = gremlin_client.get_graph_features()
print("results", results)

#
# results = gremlin_client.query("""
# mgmt = graph.openManagement()
#
#
# person = mgmt.makeVertexLabel('person').make()
# name = mgmt.makePropertyKey('name').dataType(String.class).cardinality(Cardinality.SET).make()
# birthDate = mgmt.makePropertyKey('birthDate').dataType(Long.class).cardinality(Cardinality.SINGLE).make()
# mgmt.addProperties(person, name, birthDate)
#
#
# follow = mgmt.makeEdgeLabel('follow').multiplicity(MULTI).make()
# name = mgmt.makePropertyKey('name').dataType(String.class).cardinality(Cardinality.SET).make()
# mgmt.addProperties(follow, name)
# mgmt.commit()
# """)
#
# print("results", results)
