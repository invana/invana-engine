from .base import CRUDOperationsBase
import logging
from .core.element import VertexElement

logger = logging.getLogger(__name__)


class Vertex(CRUDOperationsBase):

    def create(self, label=None, properties=None, **kwargs):
        """

        :param label:
        :param properties:
        :param kwargs: not used
        :return:
        """
        logger.debug("Creating vertex with label {label} "
                     "and properties {properties}".format(label=label, properties=properties))

        if properties is None:
            raise Exception("Vertex cannot be created with out  properties")
        _ = self.gremlin_client.g.addV(label)
        for k, v in properties.items():
            _.property(k, v)
        _vtx = _.valueMap(True).next()
        return VertexElement(_vtx, serializer=self.serializer)

    def get_or_create(self, label=None, properties=None):
        """

        :param label:
        :param properties:
        :return:
        """
        vertices = self.read_many(label=label, query=properties)
        if vertices.__len__() > 0:
            return VertexElement(vertices[0], serializer=self.serializer)
        else:
            return self.create(label=label, properties=properties)

    def update(self, vertex_id, properties=None):
        """

        :param vertex_id:
        :param properties:
        :return:
        """
        logger.debug("Updating vertex {vertex_id} with properties {properties}".format(
            vertex_id=vertex_id, properties=properties))
        properties = {} if properties is None else properties
        vtx_instance = self.filter_vertex(vertex_id=vertex_id)
        if vtx_instance is not None:
            for k, v in properties.items():
                vtx_instance.property(k, v)
            _vtx = vtx_instance.valueMap(True).next()
            return VertexElement(_vtx, serializer=self.serializer)
        return None

    def _read_one(self, vertex_id):
        """

        :param vertex_id:
        :return:
        """
        logger.debug("Finding vertex with id {vertex_id} ".format(vertex_id=vertex_id))
        filtered_data = self.gremlin_client.g.V(vertex_id)
        try:
            _ = filtered_data.valueMap(True).next()
            if _:
                return VertexElement(_, serializer=self.serializer)
        except Exception as e:
            print(e)
            pass
        return None

    def _read_many(self, label=None, query=None, limit=10, skip=0):
        logger.debug("Updating vertex with label {label} and kwargs {query}".format(label=label, query=query))
        filtered_data = self.filter_vertex(label=label, query=query, limit=limit, skip=skip)
        cleaned_data = []
        for _ in filtered_data.valueMap(True).toList():
            cleaned_data.append(
                VertexElement(_, serializer=self.serializer)
            )
        return cleaned_data

    def _delete_one(self, vertex_id):
        logger.debug("Deleting the vertex with vertex_id:{vertex_id}".format(vertex_id=vertex_id))
        self.drop(self.filter_vertex(vertex_id=vertex_id))

    def _delete_many(self, label=None, query=None):
        logger.debug("Deleting the vertex with label:{label},"
                     " query:{query}".format(label=label, query=query))
        print("=======", self.filter_vertex(label=label, query=query))
        self.drop(self.filter_vertex(label=label, query=query))

    def read_in_edge_vertices(self, vertex_id, label=None, query=None, limit=None, skip=None):
        vtx = self.filter_vertex(vertex_id=vertex_id, label=label, query=query, limit=limit, skip=skip)
        cleaned_data = []
        for _ in vtx.inE().otherV().dedup().valueMap(True).toList():
            cleaned_data.append(VertexElement(_, serializer=self.serializer))
        return cleaned_data

    def read_out_edge_vertices(self, vertex_id, label=None, query=None, limit=None, skip=None):
        vtx = self.filter_vertex(vertex_id=vertex_id, label=label, query=query, limit=limit, skip=skip)
        cleaned_data = []
        for _ in vtx.outE().otherV().dedup().valueMap(True).toList():
            cleaned_data.append(VertexElement(_, serializer=self.serializer))
        return cleaned_data
