import os 
import csv
import typing as T
from invana_engine.backend.gremlin.backend import InvanaTraversalSource
from .base import ImporterBase


class CSVImporter(ImporterBase):
    """
    This importer expects files to be in the structure:
    
    """

    nodes_file_pattern = ["*nodes.csv"]
    links_file_pattern = ["*links.csv"]

    def read_file(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return [row for row in csv_reader]
        
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
    