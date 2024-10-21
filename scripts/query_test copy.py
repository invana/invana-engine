"""
This script will import airlines data from Kevin Lawrence's book
https://github.com/krlawrence/graph/tree/master/sample-data

cd sample-data/airlines
python import_airlines_data.py
"""
import sys
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import Cardinality
from gremlin_python.process.traversal import T

g = traversal().with_remote(DriverRemoteConnection('ws://localhost:28182/gremlin','g'))
print("Initiating import: graph :", g)

# g.V().drop().iterate()
# for i in range(0, 10):
#     # result = graph.run_query("g.addV('Hello').property('name','Test').next()") 
#     print("====", i)
#     try:
#         # .property(T.id, i)
#         # g.add_v('Hello').property(Cardinality.single, 'name',f'Test - {i}').next()
#         a = g.add_v('Hello').property( 'name',f'Test - {i}').next()
#         print("===a",a)
#     except Exception as e :
#         print(e)
# try:
#     g.add_v('Hello').property('name','Test')
# except Exception as e:
#     print(e)
# g.addV('Hello').property('name', 'Test').element_map().to_list()
# count = graph.run_query("g.V().limit(10).count()") 
# print("===count", count)
# result = graph.run_query("g.V().limit(10).elementMap().toList()") 
# print("===result", result)

# result2 = g.V().elementMap().toList()
# for r in result2:
#     print("======r",r)
# print("===result2", result2)

result3 = g.V().count().next()
print("======== exit", result3)
 