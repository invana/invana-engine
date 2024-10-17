"""
This script will import airlines data from Kevin Lawrence's book
https://github.com/krlawrence/graph/tree/master/sample-data

cd sample-data/airlines
python import_airlines_data.py
"""
import sys
import os
sys.path.append(os.path.join(os.getcwd() ))
print("sys.path", sys.path)
print("os.", os.getcwd())
from invana_engine import InvanaGraph
import csv


graph = InvanaGraph()
print("Initiating import: graph :", graph)

 
result = graph.execute_query("g.addV('Hello').property('name','Test').next()") 
# graph.execute_query("g.addV('Hello').property('name', 'Test').elementMap()")
count = graph.execute_query("g.V().limit(10).count()") 
print("===count", count.data)
result = graph.execute_query("g.V().limit(10).elementMap().toList()") 
print("===result", result.data)

result2 = graph.backend.g.V().limit(10).elementMap().toList()
print("===result2", result2)

 