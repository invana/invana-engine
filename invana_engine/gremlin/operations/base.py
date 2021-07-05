import abc
from ..core.exceptions import InvalidQueryArguments, InvalidPropertiesException
from ..core.translator import GremlinQueryTranslator


class GremlinOperationBase:

    def __init__(self, gremlin_client=None):
        """

        :param gremlin_client: InvanaEngineClient instance
        """
        self.gremlin_client = gremlin_client
        self.translator = GremlinQueryTranslator()

    # @staticmethod
    # def get_namespaced_label(label=None, namespace=None):
    #     return "{}/{}".format(namespace, label) if namespace else label

    @staticmethod
    def validate_properties(properties):
        if not isinstance(properties, dict):
            raise InvalidPropertiesException(
                "properties should be passed as 'dict' type, but received '{}' type".format(type(properties)))

    @property
    def serializer(self):
        return self.gremlin_client.serializer

    @staticmethod
    def process_graph_schema_string(schema_string):
        schema = {
            "vertex_labels": [],
            "edge_labels": [],
            "property_keys": [],
        }
        data_type = None
        __count = 0
        for line in schema_string.split("\n"):
            if line.startswith("-------"):
                __count += 1
                continue
            if data_type == "vertices" and __count == 2:
                schema['vertex_labels'].append(line.split("|")[0].strip())
            elif data_type == "edges" and __count == 4:
                schema['edge_labels'].append(line.split("|")[0].strip())
            elif data_type == "properties" and __count == 6:
                schema['property_keys'].append(line.split("|")[0].strip())

            if line.startswith("Vertex Label Name"):
                data_type = "vertices"
            elif line.startswith("Edge Label Name"):
                data_type = "edges"
            elif line.startswith("Property Key Name"):
                data_type = "properties"
        return schema

    def get_graph_schema(self):
        # TODO - can add more information from the print schema data like indexes etc to current output
        result = self.gremlin_client.query("mgmt = graph.openManagement(); mgmt.printSchema()")
        return self.process_graph_schema_string(result[0])


class CRUDOperationsBase(GremlinOperationBase, metaclass=abc.ABCMeta):

    # def filter_vertex(self, vertex_id=None, label=None, query=None, limit=None, skip=None):
    #     """
    #
    #     :param vertex_id:
    #     :param label:
    #     :param namespace:
    #     :param query:
    #     :param limit:
    #     :param skip:
    #     :return:
    #     """
    #     query = {} if query is None else query
    #     _ = self.gremlin_client.g.V(vertex_id) if vertex_id else self.gremlin_client.g.V()
    #     if label:
    #         _.hasLabel(label)
    #     if query:
    #         for k, v in query.items():
    #             _.has(k, v)
    #     if limit is not None and skip is not None:  # TODO - pagination fixes needed
    #         _.range(skip, skip + limit)
    #     return _

    def filter_edge(self, edge_id=None, label=None, query=None, limit=None, skip=None):
        """

        :param edge_id:
        :param label:
        :param namespace:
        :param query:
        :param limit:
        :param skip:
        :return:
        """
        query = {} if query is None else query
        _ = self.gremlin_client.g.E(edge_id) if edge_id else self.gremlin_client.g.E()
        if label:
            _.hasLabel(label)
        for k, v in query.items():
            _.has(k, v)
        if limit is not None and skip is not None:  # TODO - pagination fixes needed
            _.range(skip, skip + limit)

        return _

    # @abc.abstractmethod
    # def create(self, label=None, properties=None, **kwargs):
    #     pass
    #
    # @abc.abstractmethod
    # def update(self, elem_id, properties=None):
    #     pass
    #
    # @abc.abstractmethod
    # def _read_one(self, element_id):
    #     pass
    #
    # def read_one(self, element_id):
    #     return self._read_one(element_id)

    # @abc.abstractmethod
    # def _read_many(self, label=None, query=None, limit=None, skip=None):
    #     pass

    # def read_many(self, label=None, query=None, limit=None, skip=None):
    #     return self._read_many(label=label, query=query, limit=limit, skip=skip)

    # @abc.abstractmethod
    # def _delete_one(self, element_id):
    #     pass

    # def delete_one(self, element_id):
    #     return self._delete_one(element_id)

    # @staticmethod
    # def validate_filter_many_filters(label=None, query=None):
    #     if label is None and query is None:
    #         raise InvalidQueryArguments("Both label and query arguments cannot be none")

    # @abc.abstractmethod
    # def _delete_many(self, label=None, query=None):
    #     pass

    # def delete_many(self, label=None, query=None):
    #     self.validate_filter_many_filters(label=label, query=query)
    #     return self._delete_many(label=label, query=query)

    # @abc.abstractmethod
    # def get_or_create(self, label=None, properties=None):
    #     pass
    # #
    # @staticmethod
    # def drop(_):
    #     _.drop().iterate()
