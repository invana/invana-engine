from invana_engine.gremlin import GremlinClient

client = GremlinClient("ws://192.168.0.10:8182/gremlin")
client.delete_everything()
print("Data completely deleted!")
