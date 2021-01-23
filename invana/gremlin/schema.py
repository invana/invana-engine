from .base import GremlinOperationBase, CRUDOperationsBase
from gremlin_python.process.strategies import *
from gremlin_python.process.traversal import Order


class SchemaOps(GremlinOperationBase):

    def get_all_vertices_schema(self):
        _ = self.gremlin_client.execute_query(
            "g.V().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )
        schema_data = []
        for schema in _:
            for k, v in schema.items():
                schema_data.append(
                    {
                        "label": k,
                        "propertyKeys": v
                    }
                )
        return schema_data

    def get_vertex_label_schema(self, label: str, namespace: str = None):
        # TODO - fix performance
        _ = self.gremlin_client.execute_query(
            "g.V().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )
        return {"label": label, "propertyKeys": _[0].get(label, [])}

    def get_all_edges_schema(self):
        _ = self.gremlin_client.execute_query(
            "g.E().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )
        schema_data = []
        for schema in _:
            for k, v in schema.items():
                schema_data.append(
                    {
                        "label": k,
                        "propertyKeys": v
                    }
                )
        return schema_data

    def get_edge_label_schema(self, label: str, namespace: str = None):
        # TODO - fix performance
        _ = self.gremlin_client.execute_query(
            "g.E().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )

        return {"label": label, "propertyKeys": _[0].get(label, [])}
