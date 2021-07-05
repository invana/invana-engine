from .base import CRUDOperationsBase
import logging
import json
from ..core.exceptions import InvalidQueryArguments
import ast

logger = logging.getLogger(__name__)


class GraphSchemaOperations(CRUDOperationsBase):

    def get_graph_schema(self):
        return self.gremlin_client.query("mgmt = graph.openManagement(); mgmt.printSchema()")

    def get_all_vertices_schema(self):
        # TODO - fix performance, this query needs full scan of the graph
        _ = self.gremlin_client.query(
            "g.V().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )
        schema_data = []
        for schema in _:
            for k, v in schema.items():
                schema_data.append({"label": k, "propertyKeys": v})
        return schema_data

    def get_all_edges_schema(self):
        # TODO - fix performance, this query needs full scan of the graph
        _ = self.gremlin_client.query(
            "g.E().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )
        schema_data = []
        for schema in _:
            for k, v in schema.items():
                schema_data.append({"label": k, "propertyKeys": v})
        return schema_data

    def get_vertex_schema(self, label):
        schema_data = self.get_all_vertices_schema()
        for label_schema in schema_data:
            if label_schema['label'] == label:
                return label_schema
        return

    def get_edge_schema(self, label):
        schema_data = self.get_all_vertices_schema()
        for label_schema in schema_data:
            if label_schema['label'] == label:
                return label_schema
        return

    def get_graph_features(self):
        _ = self.gremlin_client.query("graph.features()")[0]
        result = {}
        this_feature_name = None
        _ = _.replace("FEATURES", "")
        for feature_section in _.split("> "):
            for feature_section_item in feature_section.split("\n"):
                if feature_section_item:
                    if not feature_section_item.startswith(">--"):
                        this_feature_name = feature_section_item.strip()
                        result[this_feature_name] = {}
                    else:
                        feature_name = feature_section_item.split(":")[0].lstrip(">--").rstrip()
                        feature_status = feature_section_item.split(":")[1].strip()
                        result[this_feature_name][feature_name] = ast.literal_eval(feature_status.capitalize())
        return result
