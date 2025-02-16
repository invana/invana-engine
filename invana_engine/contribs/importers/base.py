import abc
import os
import typing as T
from pathlib import Path
from collections import defaultdict
from .exception import PathNotFound, DuplicateFileError
from invana_engine.backends.gremlin.backend import InvanaTraversalSource


class ImporterBase(abc.ABC):

    """
    
    nodes_file_pattern = ["nodes.json"] or ["nodes.csv"] or ...
    links_file_pattern = ["links.json"] or ["links.csv"] or ...
    
    """
    nodes_file_pattern = None
    links_file_pattern = None
    nodes_map : T.Dict[T.Union[int, str], T.Union[int, str]] = {}

    def __init__(self, base_path: str, invana) -> None:
        self.base_path = base_path
        self.invana = invana

        if not os.path.isdir(self.base_path):
            raise PathNotFound(f"Path '{self.base_path}' not found.")

    @abc.abstractmethod
    def read_file(self, file_path):
        pass

    def create_nodes(self, nodes):
        g: InvanaTraversalSource = self.invana.backend.g
        for node in nodes:
            node_instance = g.create_vertex(node['label'], **node['properties']).next()
            print("node_instance", node_instance)
            self.nodes_map[node['id']] = node_instance.id
                        

    def create_links(self, links):
        g: InvanaTraversalSource = self.invana.backend.g
        for link in links:
            links_instance = g.create_edge(link['label'],
                                self.nodes_map[link['from']],
                                self.nodes_map[link['to']],
                                **link['properties']
                            ).next()
            print("link_instance", links_instance)

    def scan_folder(self, folder_path):
        folder = Path(folder_path)
        
        nodes_files = []
        links_files = []

        # Collect nodes files
        for pattern in self.nodes_file_pattern:
            for node_file in folder.rglob(pattern):
                if node_file in links_files:
                    raise DuplicateFileError(f"Duplicate file found: {node_file} is in both nodes and links.")
                if node_file not in nodes_files:
                    nodes_files.append(node_file)

        # Collect links files
        for pattern in self.links_file_pattern:
            for link_file in folder.rglob(pattern):
                if link_file in nodes_files:
                    raise DuplicateFileError(f"Duplicate file found: {link_file} is in both nodes and links.")
                if link_file not in links_files:
                    links_files.append(link_file)

        return nodes_files, links_files

    def group_by_labels(self, data, clean_item_fn=None):
        data_groups = defaultdict(list)
        # Group data
        for item in data:
            item_cleaned = clean_item_fn(item) if clean_item_fn else item
            data_groups[item_cleaned['label']].append(item_cleaned)
        return data_groups


    def read_files(self):
        nodes_files, links_files = self.scan_folder(self.base_path)
        all_nodes = []
        all_links = []

        for node_file in nodes_files:
            all_nodes.extend(self.read_file(node_file))

        for link_file in links_files:
            all_links.extend(self.read_file(link_file))

        return all_nodes, all_links
    
    def start(self, clean_nodes_fn=None , clean_links_fn=None ):
        all_nodes, all_links = self.read_files()
        node_groups = self.group_by_labels(all_nodes, clean_item_fn=clean_nodes_fn)
        link_groups = self.group_by_labels(all_links, clean_item_fn=clean_links_fn)
        for label, nodes in node_groups.items():
            print(f"Found {label} \t\tnodes: {nodes.__len__()}")
            self.create_nodes(nodes)

        for label, links in link_groups.items():
            print(f"Found {label}\t\tlinks: {links.__len__()}")
            self.create_links(links)

        # print(f"Created {nodes_map.__len__()} nodes, and {links_instances.__len__()} links")

