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

 
graph.backend.g.V().drop().iterate()
for i in range(0, 1):
    a = graph.backend.g.addV('Hello').property('name',f'Test {i}').elementMap().next()
    print(a)

result = graph.backend.run_query('g.V().limit(1).toList()')
print("====result", result.data)
