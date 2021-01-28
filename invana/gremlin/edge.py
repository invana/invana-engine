from .base import CRUDOperationsBase
from .core.element import EdgeElement, VertexElement
import logging

logger = logging.getLogger(__name__)


class Edge(CRUDOperationsBase):

    def get_or_create(self, label=None, namespace=None, properties=None):
        """

        :param label:
        :param namespace:
        :param properties: {"id": 123213 }
        :return:
        """

        edges = self.read_many(label=label, namespace=namespace, query=properties)
        if edges.__len__() > 0:
            return edges[0]
        else:
            return self.create(label=label, namespace=namespace, properties=properties)

    def create(self, label=None, namespace=None, properties=None, inv=None, outv=None):
        """

        :param label:
        :param namespace:
        :param properties:
        :param inv: str or VertexElement
        :param outv: str or VertexElement
        :return:
        """
        logger.debug("Creating Edge with label {label}, namespace {namespace} and properties {properties}".format(
            label=label,
            namespace=namespace,
            properties=properties)
        )
        label = self.get_namespaced_label(label=label, namespace=namespace)
        properties = {} if properties is None else properties
        inv_vtx_instance = self.filter_vertex(inv)
        outv_vtx_instance = self.filter_vertex(outv)
        _ = inv_vtx_instance.addE(label) \
            .to(outv_vtx_instance)
        for property_key, property_value in properties.items():
            _.property(property_key, property_value)
        edg = _.elementMap().next()
        return EdgeElement(edg, serializer=self.serializer)

    def update(self, edg_id, properties=None):
        logger.debug("Updating vertex  {edg_id} with properties {properties}".format(edg_id=edg_id,
                                                                                     properties=properties, ))
        edge = self.filter_edge(edge_id=edg_id)
        properties = {} if properties is None else properties
        if edge:
            for k, v in properties.items():
                edge.property(k, v)
            _edge = edge.elementMap().next()
            return EdgeElement(_edge, serializer=self.serializer)
        return None

    def _read_one(self, edge_id):
        logger.debug("Finding edge with id {edge_id}".format(
            edge_id=edge_id))
        filtered_data = self.filter_edge(edge_id=edge_id)
        try:
            _ = filtered_data.elementMap().next()
            if _:
                return EdgeElement(_, serializer=self.serializer)
        except Exception as e:
            pass
        return None

    def _read_many(self, label=None, namespace=None, query=None, limit=10, skip=0):
        filtered_data = self.filter_edge(label=label, namespace=namespace, query=query, limit=limit, skip=skip)
        cleaned_data = []
        for _ in filtered_data.elementMap().toList():
            cleaned_data.append(EdgeElement(_, serializer=self.serializer))
        return cleaned_data

    def filter_edge_and_get_neighbor_vertices(self, edge_id=None, label=None, namespace=None, query=None, limit=None,
                                        skip=None):

        cleaned_edges_data = self._read_many(label=label, namespace=namespace,query=query, limit=limit, skip=skip)
        filtered_edges = self.filter_edge(label=label, namespace=namespace, query=query, limit=limit, skip=skip)

        vertices_data = []
        for _ in filtered_edges.inV().dedup().elementMap().toList():
            vertices_data.append(VertexElement(_, serializer=self.serializer))

        filtered_edges = self.filter_edge(label=label, namespace=namespace, query=query, limit=limit, skip=skip)

        for _ in filtered_edges.outV().dedup().elementMap().toList():
            vertices_data.append(VertexElement(_, serializer=self.serializer))
        vertices_data = list(set(vertices_data))

        return cleaned_edges_data + vertices_data


    def _delete_one(self, edge_id):
        logger.debug("Deleting the edge with edge_id:{edge_id}".format(edge_id=edge_id))
        self.drop(self.filter_edge(edge_id=edge_id))

    def _delete_many(self, label=None, namespace=None, query=None):
        logger.debug("Deleting the edges with label:{label} namespace:{namespace},"
                     " query:{query}".format(label=label, query=query, namespace=namespace))
        self.drop(self.filter_edge(label=label, namespace=namespace, query=query))
