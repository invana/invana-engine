from .base import GremlinOperationBase, CRUDOperationsBase


class ManagementOps(GremlinOperationBase):

    def get_vertices_label_stats(self, label: str = None, namespace: str = None, limit: int = None, order: str = None):
        stats = self.gremlin_client.g.V().label().groupCount().next()
        label_stats = []
        for label, count in stats.items():
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
