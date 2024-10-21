"""
This script will import airlines data from Kevin Lawrence's book
https://github.com/krlawrence/graph/tree/master/sample-data

cd sample-data/airlines
python import_airlines_data.py
"""
import sys
import os
sys.path.append(os.path.join(os.getcwd() ))
from invana_engine import InvanaGraph
import csv


graph = InvanaGraph()
print("Initiating import: graph :", graph)

 
for i in range(0, 10):
    result = graph.run_query("g.addV('Hello').property('name','Test').next()") 
# graph.execute_query("g.addV('Hello').property('name', 'Test').elementMap()")
count = graph.run_query("g.V().limit(10).count()") 
print("===count", count)
result = graph.run_query("g.V().limit(10).elementMap().toList()") 
print("===result", result)

result2 = graph.backend.g.V().limit(10).elementMap().toList()
print("===result2", result2)

 