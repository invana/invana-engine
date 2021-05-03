from invana_engine.gremlin import InvanaEngineClient

client = InvanaEngineClient("ws://192.168.0.10:8182/gremlin")
data = client.vertex.read_many()
print("Data is", data, data.__dict__())
