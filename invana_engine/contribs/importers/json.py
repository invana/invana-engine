import os 
import json
import typing as T
from invana_engine.backend.gremlin.backend import InvanaTraversalSource
from .exception import PathNotFound
from .base import ImporterBase


class JSONImporter(ImporterBase):
    """
    This importer expects files to be in the structure:
 
    
    """
    nodes_file_pattern = ["*nodes.json"]
    links_file_pattern = ["*links.json"]

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
        
    def create_nodes(self, nodes):
        g: InvanaTraversalSource = self.invana.backend.g
        for node in nodes:
            node_instance = g.create_vertex(node['label'], **node['properties']).next()
            self.nodes_map[node['id']] = node_instance.id
                        

    def create_links(self, links):
        g: InvanaTraversalSource = self.invana.backend.g
        for link in links:
            links_instance = g.create_edge(link['label'],
                                self.nodes_map[link['from']],
                                self.nodes_map[link['to']],
                                **link['properties']
                            )
    