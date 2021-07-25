from .base import CRUDOperationsBase
import logging
from .core.element import VertexElement, EdgeElement
from ..server.utils import get_unique_items

logger = logging.getLogger(__name__)


class Vertex(CRUDOperationsBase):

    def create(self, label=None, namespace=None, properties=None, **kwargs):
        """

        :param label:
        :param namespace:
        :param properties:
        :param kwargs: not used
        :return:
        """
        logger.debug("Creating vertex with label {label} namespace {namespace}"
                     "and properties {properties}".format(label=label, namespace=namespace, properties=properties))
        label = self.get_namespaced_label(label=label, namespace=namespace)

        if properties is None:
            raise Exception("Vertex cannot be created with out  properties")
        _ = self.gremlin_client.g.addV(label)
        for k, v in properties.items():
            _.property(k, v)
        _vtx = _.elementMap().next()
        return VertexElement(_vtx, serializer=self.serializer)

    def get_or_create(self, label=None, namespace=None, properties=None):
        """

        :param label:
        :param namespace:
        :param properties:
        :return:
        """
        vertices = self.read_many(label=label, namespace=namespace, query=properties)
        if vertices.__len__() > 0:
            # return VertexElement(vertices[0], serializer=self.serializer)
            return vertices[0]
        else:
            return self.create(label=label, namespace=namespace, properties=properties)

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
            _vtx = vtx_instance.elementMap().next()
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
            _ = filtered_data.elementMap().next()
            if _:
                return VertexElement(_, serializer=self.serializer)
        except Exception as e:
            print(e)
            pass
        return None

    def _read_many(self, label=None, namespace=None, query=None, limit=10, skip=0):
        logger.debug("Reading vertices with label:{label}; namespace:{namespace}; query: {query}; limit: {limit}"
                     "; skip: {skip}".format(label=label, namespace=namespace, query=query, limit=limit, skip=skip))
        filtered_data = self.filter_vertex(label=label, namespace=namespace, query=query, limit=limit, skip=skip)
        cleaned_data = []
        for _ in filtered_data.elementMap().toList():
            cleaned_data.append(
                VertexElement(_, serializer=self.serializer)
            )
        return cleaned_data

    def _delete_one(self, vertex_id):
        logger.debug("Deleting the vertex with vertex_id:{vertex_id}".format(vertex_id=vertex_id))
        self.drop(self.filter_vertex(vertex_id=vertex_id))

    def _delete_many(self, label=None, namespace=None, query=None):
        logger.debug("Deleting the vertex with label:{label}, namespace:{namespace}"
                     " query:{query}".format(label=label, namespace=namespace, query=query))
        self.drop(self.filter_vertex(label=label, namespace=namespace, query=query))

    def read_in_edges_and_vertices(self, vertex_id, label=None, namespace=None, query=None, limit=None, skip=None):
        # TODO - fix the performance, filter queries are made twice
        vtx = self.filter_vertex(vertex_id=vertex_id, label=label, namespace=namespace,
                                 query=query, limit=limit, skip=skip)
        cleaned_data = []
        for _ in vtx.inE().dedup().elementMap().toList():
            cleaned_data.append(EdgeElement(_, serializer=self.serializer))
        vtx = self.filter_vertex(vertex_id=vertex_id, label=label, namespace=namespace,
                                 query=query, limit=limit, skip=skip)
        for _ in vtx.inE().otherV().dedup().elementMap().toList():
            cleaned_data.append(VertexElement(_, serializer=self.serializer))
        return cleaned_data

    def read_out_edges_and_vertices(self, vertex_id, label=None, namespace=None, query=None, limit=None, skip=None):
        # TODO - fix the performance, filter queries are made twice
        vtx = self.filter_vertex(vertex_id=vertex_id, label=label, namespace=namespace,
                                 query=query, limit=limit, skip=skip)
        cleaned_data = []
        for _ in vtx.outE().dedup().elementMap().toList():
            cleaned_data.append(EdgeElement(_, serializer=self.serializer))
        vtx = self.filter_vertex(vertex_id=vertex_id, label=label, namespace=namespace,
                                 query=query, limit=limit, skip=skip)
        for _ in vtx.outE().otherV().dedup().elementMap().toList():
            cleaned_data.append(VertexElement(_, serializer=self.serializer))
        return cleaned_data

    def filter_vertex_and_neighbor_edges_and_vertices(self, vertex_id=None, label=None, namespace=None, query=None, limit=None,
                                        skip=None):
        cleaned_data = []
        vertices = self.filter_vertex(vertex_id=vertex_id, label=label, namespace=namespace,
                                      query=query, limit=limit, skip=skip)
        for _ in vertices.dedup().elementMap().toList():
            cleaned_data.append(VertexElement(_, serializer=self.serializer))

        # TODO - fix the performance, filter queries are made twice (damn! now increased to 5 times)
        in_edges_and_vertices = self.read_in_edges_and_vertices(vertex_id=vertex_id, label=label, namespace=namespace,
                                                                query=query, limit=limit, skip=skip)
        cleaned_data.extend(in_edges_and_vertices)
        out_edges_and_vertices = self.read_out_edges_and_vertices(vertex_id=vertex_id, label=label, namespace=namespace,
                                                                  query=query, limit=limit, skip=skip)
        cleaned_data.extend(out_edges_and_vertices)
        unique_elements = get_unique_items(cleaned_data)
        return unique_elements
