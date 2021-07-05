from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal

connection = DriverRemoteConnection("ws://localhost:8182/gremlin", "g")
g = traversal().withRemote(connection)

result = g.V().valueMap(True).limit(1).next()
connection.close()
