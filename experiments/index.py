from invana_engine.gremlin.client import GremlinClient

gremlin_client = GremlinClient("ws://192.168.0.10:8182/gremlin")

gremlin_client.indexes.composite_index.create_vertex_index(
    "byNameRadiusPlanet", "Planet", ["name", "radius_in_kms"]
)
