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
from invana_engine.backends import InvanaTraversalSource, GremlinBackend
import csv

invana = InvanaGraph()
print("Initiating import: invana :", invana)


def clean_nodes(node_data):
    cleaned_data = {}
    for k, v in node_data.items():
        if k.startswith("~"):
            cleaned_data[k.lstrip('~')] = v
        elif ":" in k:
            cleaned_data[k.split(":")[0]] = v

    _id = cleaned_data['id']
    _label = cleaned_data['label']
    del cleaned_data['id']
    del cleaned_data['label']
    return {
        "id": _id,
        "label": _label,
        "properties": cleaned_data
    }

def clean_edges(edge_data):
    cleaned_data = {}
    for k, v in edge_data.items():
        if k.startswith("~"):
            cleaned_data[k.lstrip('~')] = v
        elif ":" in k:
            cleaned_data[k.split(":")[0]] = v

    _id = cleaned_data['id']
    _label = cleaned_data['label']
    _from = cleaned_data['from']
    _to = cleaned_data['to']
    del cleaned_data['id']
    del cleaned_data['label']
    del cleaned_data['from']
    del cleaned_data['to']
    return {
        "id": _id,
        "label": _label,
        "from": _from,
        "to": _to,
        "properties": cleaned_data
    }

node_id_map = {}
backend: GremlinBackend = invana.backend
backend.g.V().drop().iterate()


with open(os.path.join(os.getcwd() ,'./sample-data/airlines/air-routes-latest-nodes.csv')) as f:
    reader = csv.DictReader(f)
    for line in reader:
        cleaned_data = clean_nodes(line)
        created_data = backend.g.create_vertex(cleaned_data['label'], **cleaned_data['properties']).next()
        print(f"**created node {created_data}")
        node_id_map[cleaned_data['id']] = created_data.id

with open(os.path.join(os.getcwd() ,'./sample-data/airlines/air-routes-latest-edges.csv')) as f:
    reader = csv.DictReader(f)
    g: InvanaTraversalSource = backend.g
    for line in reader:
        cleaned_data = clean_edges(line)
        created_data = g.create_edge(cleaned_data['label'],
                                         node_id_map[cleaned_data['from']],
                                         node_id_map[cleaned_data['to']],
                                         **cleaned_data['properties']).elementMap().next()
        print(f"**created edge {created_data.id}")
