from .base import CRUDOperationsBase
from .core.element import EdgeElement
import logging

logger = logging.getLogger(__name__)


class Edge(CRUDOperationsBase):

    def get_or_create(self, label=None, query=None):
        """

        :param label:
        :param query: {"id": 123213 }
        :return:
        """

        edges = self.read_many(label=label, query=query)
        if edges.__len__() > 0:
            return edges[0]
        else:
            return self.create(label=label, properties=query)

    def create(self, label=None, properties=None, inv=None, outv=None):
        """

        :param label:
        :param properties:
        :param inv: str or VertexElement
        :param outv: str or VertexElement
        :return:
        """
        logger.debug("Creating Edge with label {label} and properties {properties}".format(
            label=label,
            properties=properties)
        )
        properties = {} if properties is None else properties
        inv_vtx_instance = self.filter_vertex(inv)
        outv_vtx_instance = self.filter_vertex(outv)
        _ = inv_vtx_instance.addE(label) \
            .to(outv_vtx_instance)
        for property_key, property_value in properties.items():
            _.property(property_key, property_value)
        edg = _.valueMap(True).next()
        return EdgeElement(edg, serializer=self.serializer)

    def update(self, edg_id, properties=None):
        logger.debug("Updating vertex  {edg_id} with properties {properties}".format(edg_id=edg_id,
                                                                                     properties=properties, ))
        edge = self.filter_edge(edge_id=edg_id)
        properties = {} if properties is None else properties
        if edge:
            for k, v in properties.items():
                edge.property(k, v)
            _edge = edge.valueMap(True).next()
            return EdgeElement(_edge, serializer=self.serializer)
        return None

    def _read_one(self, edge_id):
        logger.debug("Finding edge with id {edge_id}".format(
            edge_id=edge_id))
        filtered_data = self.filter_edge(edge_id=edge_id)
        try:
            _ = filtered_data.valueMap(True).next()
            if _:
                return EdgeElement(_, serializer=self.serializer)
        except Exception as e:
            pass
        return None

    def _read_many(self, label=None, query=None, limit=10, skip=0):
        filtered_data = self.filter_edge(label=label, query=query)
        cleaned_data = []
        for _ in filtered_data.valueMap(True).toList():
            cleaned_data.append(EdgeElement(_, serializer=self.serializer))
        return cleaned_data

    def _delete_one(self, edge_id):
        logger.debug("Deleting the edge with edge_id:{edge_id}".format(edge_id=edge_id))
        self.drop(self.filter_edge(edge_id=edge_id))

    def _delete_many(self, label=None, query=None):
        logger.debug("Deleting the vertex with label:{label},"
                     " query:{query}".format(label=label, query=query))
        self.drop(self.filter_edge(label=label, query=query))
