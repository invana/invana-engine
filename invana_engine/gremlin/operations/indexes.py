from .base import CRUDOperationsBase
import logging
import json
from ..core.exceptions import InvalidQueryArguments
import ast

logger = logging.getLogger(__name__)


class GraphIndexOperations(CRUDOperationsBase):
    pass
    # def create_composite_index(self, label):
    #     result = self.gremlin_client.query("g.V().hasLabel('{}').count()".format(label))
    #     return result[0]
    #
    # def get_edge_stats(self, label):
    #     result = self.gremlin_client.query("g.E().hasLabel('{}').count()".format(label))
    #     return result[0]
