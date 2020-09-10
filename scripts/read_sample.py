from invana.gremlin import GremlinClient

client = GremlinClient("ws://192.168.0.10:8182/gremlin")
data = client.vertex.read_one(element_id=98528)
print("Data is", data, data.__dict__())
