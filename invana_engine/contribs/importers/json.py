import os 
import json
import typing as T
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
        

    