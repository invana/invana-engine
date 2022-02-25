"""
This script will import airlines data from Kevin Lawrence's book
https://github.com/krlawrence/graph/tree/master/sample-data

"""

from invana import InvanaGraph
import csv

graph = InvanaGraph("ws://megamind-ws:8182/gremlin")
print("Initiating import: graph :", graph)


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

with open('./air-routes-latest-nodes.csv') as f:
    reader = csv.DictReader(f)
    for line in reader:
        cleaned_data = clean_nodes(line)
        created_data = graph.vertex.create(cleaned_data['label'], **cleaned_data['properties']).to_list()
        print("created_data", created_data[0].id)
        node_id_map[cleaned_data['id']] = created_data[0].id

with open('./air-routes-latest-edges.csv') as f:
    reader = csv.DictReader(f)
    for line in reader:
        cleaned_data = clean_edges(line)
        created_data = graph.edge.create(label=cleaned_data['label'],
                                                inv=node_id_map[cleaned_data['to']],
                                                outv=node_id_map[cleaned_data['from']],
                                                properties=cleaned_data['properties']).to_list()
        print("created_data", created_data[0].id)
