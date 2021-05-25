"""


"""

from invana_engine.gremlin.client import InvanaEngineClient

client = InvanaEngineClient(gremlin_server_url="ws://192.168.0.10:8182/gremlin")
print("Initiating import: client :", client)

client.execute_query("g.V().hasLabel(\"Planet\").drop()")

earth_label = "Planet"
earth_properties = {
    "name": "Earth",
    "radius_in_kms": 6378,
}

earth_data = client.vertex.create(
    label=earth_label,
    properties=earth_properties
)

print(earth_data, type(earth_data))

earth_new_properties = {
    "average_orbital_speed_in_kms": 29.78
}
earth_data_updated = client.vertex.update(earth_data.id, properties=earth_new_properties)

# read_one
earth_data = client.vertex.read_one(earth_data.id)
planets_data = client.vertex.read_many(label="Planet", query={"name": "Earth"})

print(planets_data)

_ = client.vertex.read_in_edges_and_vertices(earth_data.id)
print("------", _)
