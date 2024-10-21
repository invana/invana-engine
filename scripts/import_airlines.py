from invana_engine.contribs.importers import CSVImporter
from invana_engine.graph import InvanaGraph
import os

invana = InvanaGraph()
invana.drop()
importer = CSVImporter(os.path.join(os.getcwd(), "sample-data/airlines/"), invana)


def clean_nodes(node):
    cleaned_data = {}
    for k, v in node.items():
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

def clean_links(link):
    cleaned_data = {}
    for k, v in link.items():
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

importer.start(clean_nodes_fn=clean_nodes, clean_links_fn=clean_links)