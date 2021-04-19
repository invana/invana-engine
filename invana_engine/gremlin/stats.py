from .base import GremlinOperationBase
from invana_engine.server.settings import MANAGEMENT_VERTEX_NAME


class StatsOps(GremlinOperationBase):

    def get_vertices_label_stats(self, label: str = None, namespace: str = None, limit: int = None, order: str = None):
        stats = self.gremlin_client.g.V().label().groupCount().next()
        label_stats = []
        for label, count in stats.items():
            if label != MANAGEMENT_VERTEX_NAME:

                if namespace:
                    if "{}/".format(namespace) in label:
                        label_stats.append({"label": label, "count": count})
                else:
                    label_stats.append({"label": label, "count": count})

        return label_stats

    def get_edges_label_stats(self, label: str = None, namespace: str = None, limit: int = None, order: str = None):
        stats = self.gremlin_client.g.E().label().groupCount().next()
        label_stats = []
        for label, count in stats.items():
            if namespace:
                if "{}/".format(namespace) in label:
                    label_stats.append({"label": label, "count": count})
            else:
                label_stats.append({"label": label, "count": count})
        return label_stats

    def get_vertex_label_stats(self, label: str, namespace: str = None):
        _ = self.gremlin_client.g.V().hasLabel(label).count().next()
        return {"label": label, "count": _}

    def get_edge_label_stats(self, label: str, namespace: str = None):
        _ = self.gremlin_client.g.E().hasLabel(label).count().next()
        return {"label": label, "count": _}

    # def get_all_vertices_schema(self):
    #     _ = self.gremlin_client.execute_query(
    #         "g.V().group().by(label).by(properties().label().dedup().fold())",
    #         serialize_elements=False
    #     )
    #     schema_data = []
    #     for schema in _:
    #         for k, v in schema.items():
    #             schema_data.append(
    #                 {
    #                     "label": k,
    #                     "propertyKeys": v
    #                 }
    #             )
    #     return schema_data
    #
    # def get_vertex_label_schema(self, label: str, namespace: str = None):
    #     # TODO - fix performance
    #     _ = self.gremlin_client.execute_query(
    #         "g.V().group().by(label).by(properties().label().dedup().fold())",
    #         serialize_elements=False
    #     )
    #     return {"label": label, "propertyKeys": _[0].get(label, [])}
    #
    # def get_all_edges_schema(self):
    #     _ = self.gremlin_client.execute_query(
    #         "g.E().group().by(label).by(properties().label().dedup().fold())",
    #         serialize_elements=False
    #     )
    #     schema_data = []
    #     for schema in _:
    #         for k, v in schema.items():
    #             schema_data.append(
    #                 {
    #                     "label": k,
    #                     "propertyKeys": v
    #                 }
    #             )
    #     return schema_data
    #
    # def get_edge_label_schema(self, label: str, namespace: str = None):
    #     # TODO - fix performance
    #     _ = self.gremlin_client.execute_query(
    #         "g.E().group().by(label).by(properties().label().dedup().fold())",
    #         serialize_elements=False
    #     )
    #
    #     return {"label": label, "propertyKeys": _[0].get(label, [])}
    #
