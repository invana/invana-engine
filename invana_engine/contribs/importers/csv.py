import os 
import csv
import typing as T
from invana_engine.backends.gremlin.backend import InvanaTraversalSource
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

