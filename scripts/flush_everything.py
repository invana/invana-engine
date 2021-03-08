from invana_engine.gremlin import InvanaEngineClient

client = InvanaEngineClient("ws://192.168.0.10:8182/gremlin")
client.delete_everything()
print("Data completely deleted!")
