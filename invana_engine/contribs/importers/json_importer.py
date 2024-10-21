import os 
import json
import typing as T
from invana_engine.backend.gremlin.backend import InvanaTraversalSource
from .exception import PathNotFound
from .base import ImporterBase



class JSONImporter(ImporterBase):
    """
    This importer expects files to be in the structure:

    <path>/nodes.json
    <path>/links.json
    
    """

    base_path: str = None

    nodes_file_pattern = ["nodes.json"]
    links_file_pattern = ["links.json"]
    nodes_map : T.Dict[T.Union[int, str], T.Union[int, str]] = {}

    def __init__(self, base_path: str, invana) -> None:
        self.base_path = base_path
        self.invana = invana

        if not os.path.isdir(self.base_path):
            raise PathNotFound(f"Path '{self.base_path}' not found.")
        self.nodes_file = os.path.join(self.base_path, "nodes.json")
        self.edges_file = os.path.join(self.base_path, "links.json")

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
    
    def _start(self):
        g: InvanaTraversalSource = self.invana.backend.g
        with open(self.nodes_file, 'r') as file:
            nodes = json.load(file)
        with open(self.edges_file, 'r') as file:
            links = json.load(file)
        
        nodes_map = {} # nodeid: 
        
        for node in nodes:
            node_instance = g.create_vertex(node['label'], **node['properties']).next()
            nodes_map[node['id']] = node_instance.id
        
        links_instances = []
        for link in links:
            links_instance = g.create_edge(node['label'],
                        nodes_map[link['from']],
                        nodes_map[link['to']],
                        **node['properties'])
            links_instances.append(links_instance)
        
        print(f"Created {nodes_map.__len__()} nodes, and {links_instances.__len__()} links")
 