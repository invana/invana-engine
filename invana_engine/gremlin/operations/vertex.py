#  Copyright 2020 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from .base import CRUDOperationsBase
import logging
import json
from ..core.exceptions import InvalidQueryArguments

logger = logging.getLogger(__name__)


class VertexOperations(CRUDOperationsBase):

    def create(self, label=None, properties=None):
        """
        :param label:
        :param properties:
        :return:
        """
        logger.debug(
            "Creating vertex with label {label} and properties {properties}".format(label=label, properties=properties))
        if None in [label, properties]:
            raise Exception("Vertex cannot be created with out label and properties")
        self.validate_properties(properties)
        query_string = "g.addV('{}')".format(label)
        query_string += self.translator.generate_gremlin_query_for_properties(**properties)
        query_string += ".toList()"

        _ = self.gremlin_client.query(query_string, serialize_elements=True)
        return _[0] if _ else None

    def get_or_create(self, label=None, properties=None):
        """

        :param label:
        :param properties:
        :return:
        """
        if None in [properties, label]:
            raise Exception("Vertex get_or_create methods expects label and properties data")
        self.validate_properties(properties)
        search_kwargs = {"has__label": label}
        search_kwargs.update(self.translator.convert_properties_to_query(**properties))
        vertices = self.read_many(**search_kwargs)
        if vertices.__len__() > 0:
            return vertices[0]
        return self.create(label=label, properties=properties)

    def update_one(self, vertex_id, properties=None):
        """
        :param vertex_id:
        :param properties:
        :return:
        """
        logger.debug("Updating vertex {vertex_id} with properties {properties}".format(
            vertex_id=vertex_id, properties=properties))
        properties = {} if properties is None else properties
        if vertex_id is None:
            raise InvalidQueryArguments("vertex_id should be sent for updating one vertex")
        query_string = self.translator.process_search_kwargs(has__id=vertex_id, element_type="V")
        query_string += self.translator.generate_gremlin_query_for_properties(**properties)
        return self.gremlin_client.query(query_string, serialize_elements=True)[0]

    def update_many(self, properties=None, **search_kwargs):
        """
        :param properties: properties key value pairs to be updated
        :param search_kwargs: search query kwargs to work with invana_engine.gremlin.core.translator.GremlinQueryTranslator
        :return:
        """
        logger.debug("Updating vertex with search_kwargs{search_kwargs} with properties {properties}".format(
            search_kwargs=search_kwargs, properties=properties))
        properties = {} if properties is None else properties
        query_string = self.translator.process_search_kwargs(element_type="V", **search_kwargs)
        query_string += self.translator.generate_gremlin_query_for_properties(**properties)
        return self.gremlin_client.query(query_string + ".valueMap(true).toList()", serialize_elements=True)

    def read_many(self, **search_kwargs):
        self.translator.validate_search_kwargs(**search_kwargs)
        query_string = self.translator.process_search_kwargs(element_type="V", **search_kwargs)
        return self.gremlin_client.query(query_string + ".valueMap(true).toList()", serialize_elements=True)

    def read_one(self, vertex_id):
        if vertex_id is None:
            raise InvalidQueryArguments("vertex_id should be passed for reading one vertex")
        query_string = self.translator.process_search_kwargs(has__id=vertex_id, element_type="V")
        _ = self.gremlin_client.query(query_string + ".valueMap(true).toList()", serialize_elements=True)
        if _.__len__() > 0:
            return _[0]
        return None

    def delete_one(self, vertex_id):
        logger.debug("Deleting the vertex with vertex_id:{vertex_id}".format(vertex_id=vertex_id))
        if vertex_id is None:
            raise InvalidQueryArguments("vertex_id should be sent for deleting one vertex")
        query_string = self.translator.process_search_kwargs(has__id=vertex_id, element_type="V")
        return self.gremlin_client.query(query_string + ".drop()")

    def delete_many(self, **search_kwargs):
        logger.debug("Deleting the vertex with search_kwargs:  {}".format(json.dumps(search_kwargs)))
        self.translator.validate_search_kwargs(**search_kwargs)
        query_string = self.translator.process_search_kwargs(element_type="V", **search_kwargs)
        return self.gremlin_client.query(query_string + ".drop()")

    # def read_in_edges_and_vertices(self, vertex_id, label=None,  query=None, limit=None, skip=None):
    #     # TODO - fix the performance, filter queries are made twice
    #     vtx = self.filter_vertex(vertex_id=vertex_id, label=label,
    #                              query=query, limit=limit, skip=skip)
    #     cleaned_data = []
    #     for _ in vtx.inE().dedup().elementMap().toList():
    #         cleaned_data.append(EdgeElement(_, serializer=self.serializer))
    #     vtx = self.filter_vertex(vertex_id=vertex_id, label=label,
    #                              query=query, limit=limit, skip=skip)
    #     for _ in vtx.inE().otherV().dedup().elementMap().toList():
    #         cleaned_data.append(VertexElement(_, serializer=self.serializer))
    #     return cleaned_data
    #
    # def read_out_edges_and_vertices(self, vertex_id, label=None, query=None, limit=None, skip=None):
    #     # TODO - fix the performance, filter queries are made twice
    #     vtx = self.filter_vertex(vertex_id=vertex_id, label=label,
    #                              query=query, limit=limit, skip=skip)
    #     cleaned_data = []
    #     for _ in vtx.outE().dedup().elementMap().toList():
    #         cleaned_data.append(EdgeElement(_, serializer=self.serializer))
    #     vtx = self.filter_vertex(vertex_id=vertex_id, label=label,
    #                              query=query, limit=limit, skip=skip)
    #     for _ in vtx.outE().otherV().dedup().elementMap().toList():
    #         cleaned_data.append(VertexElement(_, serializer=self.serializer))
    #     return cleaned_data
    #
    # def filter_vertex_and_neighbor_edges_and_vertices(self, vertex_id=None, label=None,  query=None,
    #                                                   limit=None, skip=None):
    #     cleaned_data = []
    #     vertices = self.filter_vertex(vertex_id=vertex_id, label=label,
    #                                   query=query, limit=limit, skip=skip)
    #     for _ in vertices.dedup().elementMap().toList():
    #         cleaned_data.append(VertexElement(_, serializer=self.serializer))
    #
    #     # TODO - fix the performance, filter queries are made twice (damn! now increased to 5 times)
    #     in_edges_and_vertices = self.read_in_edges_and_vertices(vertex_id=vertex_id, label=label,
    #                                                             query=query, limit=limit, skip=skip)
    #     cleaned_data.extend(in_edges_and_vertices)
    #     out_edges_and_vertices = self.read_out_edges_and_vertices(vertex_id=vertex_id, label=label,
    #                                                               query=query, limit=limit, skip=skip)
    #     cleaned_data.extend(out_edges_and_vertices)
    #     unique_elements = get_unique_items(cleaned_data)
    #     return unique_elements
