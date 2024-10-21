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
    # result = graph.run_query("g.addV('Hello').property('name','Test').next()") 
    print("====", i)
    a = graph.backend.g.addV('Hello').property('name',f'Test {i}').elementMap().next()
    print(a)


result2 = graph.backend.g.V().limit(1).elementMap().toList()
for r in result2:
    print("===r", r)
 