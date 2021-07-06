from ..core.exceptions import InvalidQueryArguments
from .base import CRUDOperationsBase
import logging
import json

logger = logging.getLogger(__name__)


class EdgeOperations(CRUDOperationsBase):

    def create(self, label, properties, _from, _to):
        """

        :param label:
        :param properties: dict or
        :param _to: str or int
        :param _from: str or int
        :return:
        """
        logger.debug("Creating edge with label {label} with _to {_to}, _from {_from} and"
                     " properties {properties}".format(label=label, properties=properties,
                                                       _from=_from, _to=_to))
        if None in [label, properties, _from, _to]:
            raise Exception("all params label, properties, _from, _to are required ")
        self.validate_properties(properties)
        query_string = "g.addE('{label}').from(V({_from})).to(V({_to}))".format(_to=_to, label=label, _from=_from)
        query_string += self.translator.generate_gremlin_query_for_properties(**properties)
        query_string += ".valueMap(true).toList()"
        return self.gremlin_client.query(query_string, serialize_elements=True)[0]

    def get_or_create(self, label, properties, _from, _to):
        """

        :param label:
        :param properties:
        :param _from:
        :param _to:
        :return:
        """
        if None in [properties, label, _from, _to]:
            raise Exception("all params label, properties, _from, _to are required ")
        self.validate_properties(properties)
        search_kwargs = {"has__label": label}
        search_kwargs.update(self.translator.convert_properties_to_query(**properties))
        edges = self.read_many(_from, _to, **search_kwargs)
        if edges and edges.__len__() > 0:
            return edges[0]
        return self.create(label, properties, _from, _to)

    def update_one(self, edge_id, properties=None):
        logger.debug("Updating edge {edge_id} with properties {properties}".format(edge_id=edge_id,
                                                                                   properties=properties, ))
        properties = {} if properties is None else properties
        if edge_id is None:
            raise InvalidQueryArguments("edge_id should be passed for updating one edge")
        query_string = self.translator.process_search_kwargs(has__id=edge_id, element_type="E")
        # query_string = "g.E('{}')".format(edge_id)
        query_string += self.translator.generate_gremlin_query_for_properties(**properties)

        # query_string_ = self.translator.process_search_kwargs(has__id=edge_id, element_type="E")

        # query_string += ";g.V('{}').valueMap(true).toList()".format(edge_id)
        query_string += ".valueMap(true).toList()"
        return self.gremlin_client.query(query_string, serialize_elements=True)[0]

    def update_many(self, properties=None, **search_kwargs):
        """
        :param properties: properties key value pairs to be updated
        :param search_kwargs: search query kwargs to work with invana_engine.gremlin.core.translator.GremlinQueryTranslator
        :return:
        """
        logger.debug("Updating edges with search_kwargs{search_kwargs} with properties {properties}".format(
            search_kwargs=search_kwargs, properties=properties))
        properties = {} if properties is None else properties
        query_string = self.translator.process_search_kwargs(element_type="E", **search_kwargs)
        query_string += self.translator.generate_gremlin_query_for_properties(**properties)
        return self.gremlin_client.query(query_string + ".valueMap(true).toList()", serialize_elements=True)

    def read_many(self, _from=None, _to=None, **search_kwargs):
        self.translator.validate_search_kwargs(**search_kwargs)
        _filters_string = self.translator.process_search_kwargs(element_type="E", **search_kwargs).lstrip("g.E().")
        if _from and _to:
            query_string = """g.V({_from}).outE().{_filters_string}.where(inV().hasId({_to}))        
            """.format(_from=_from, _to=_to, _filters_string=_filters_string)
        elif _from and not _to:
            query_string = """g.V({_from}).outE().{_filters_string}       
            """.format(_from=_from, _to=_to, _filters_string=_filters_string)
        elif not _from and _to:
            query_string = """g.V({_to}).inE().{_filters_string}       
            """.format(_from=_from, _to=_to, _filters_string=_filters_string)
        else:
            query_string = """g.E().{_filters_string}       
            """.format(_from=_from, _to=_to, _filters_string=_filters_string)

        _ = self.gremlin_client.query(query_string + ".valueMap(true).toList()", serialize_elements=True)
        return _

    def read_one(self, edge_id):
        if edge_id is None:
            raise InvalidQueryArguments("edge_id should be sent for reading one edge")
        query_string = self.translator.process_search_kwargs(has__id=edge_id, element_type="E")
        query_string += ".valueMap(true).toList()"
        _ = self.gremlin_client.query(query_string, serialize_elements=True)
        if _.__len__() > 0:
            return _[0]
        return None

    def delete_one(self, edge_id):
        logger.debug("Deleting the edge with edge_id:{edge_id}".format(edge_id=edge_id))
        if edge_id is None:
            raise InvalidQueryArguments("edge_id should be sent for deleting one edge")
        query_string = self.translator.process_search_kwargs(has__id=edge_id, element_type="E")
        self.gremlin_client.query(query_string + ".drop()")
        return None

    def delete_many(self, **search_kwargs):
        logger.debug("Deleting the edge with search_kwargs:  {}".format(json.dumps(search_kwargs)))
        self.translator.validate_search_kwargs(**search_kwargs)
        query_string = self.translator.process_search_kwargs(element_type="E", **search_kwargs)
        self.gremlin_client.query(query_string + ".drop()")
        return None

    # def filter_edge_and_get_neighbor_vertices(self, edge_id=None, label=None, query=None, limit=None,
    #                                           skip=None):
    #     cleaned_edges_data = self._read_many(label=label, query=query, limit=limit, skip=skip)
    #     filtered_edges = self.filter_edge(label=label, query=query, limit=limit, skip=skip)
    #
    #     vertices_data = []
    #     for _ in filtered_edges.inV().dedup().elementMap().toList():
    #         vertices_data.append(VertexElement(_, serializer=self.serializer))
    #
    #     filtered_edges = self.filter_edge(label=label, query=query, limit=limit, skip=skip)
    #
    #     for _ in filtered_edges.outV().dedup().elementMap().toList():
    #         vertices_data.append(VertexElement(_, serializer=self.serializer))
    #     vertices_data = list(set(vertices_data))
    #
    #     return cleaned_edges_data + vertices_data
