from .base import CRUDOperationsBase
import logging
import json
from ..core.exceptions import InvalidQueryArguments
import ast

logger = logging.getLogger(__name__)


class GraphStatsOperations(CRUDOperationsBase):

    def get_all_vertex_stats(self):
        schema_data = self.get_graph_schema()
        data = {}
        for vertex_label in schema_data['vertex_labels']:
            data[vertex_label] = self.get_vertex_stats(vertex_label)
        return data

    def get_all_edge_stats(self):
        schema_data = self.get_graph_schema()
        data = {}
        for edge_label in schema_data['edge_labels']:
            data[edge_label] = self.get_edge_stats(edge_label)
        return data

    def get_vertex_stats(self, label):
        result = self.gremlin_client.query("g.V().hasLabel('{}').count()".format(label))
        return result[0]

    def get_edge_stats(self, label):
        result = self.gremlin_client.query("g.E().hasLabel('{}').count()".format(label))
        return result[0]
