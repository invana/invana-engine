import abc
from .core.exceptions import InvalidQueryArguments


class CRUDOperationsBase(metaclass=abc.ABCMeta):

    def __init__(self, gremlin_client=None):
        """

        :param gremlin_client: GremlinClient instance
        """
        self.gremlin_client = gremlin_client

    @property
    def serializer(self):
        return self.gremlin_client.serializer

    def filter_vertex(self, vertex_id=None, label=None, query=None, limit=None, skip=None):
        """

        :param vertex_id:
        :param label:
        :param query:
        :param limit:
        :param skip:
        :return:
        """

        query = {} if query is None else query
        _ = self.gremlin_client.g.V(vertex_id) if vertex_id else self.gremlin_client.g.V()
        if limit and skip:  # TODO - pagination fixes needed
            _.range(skip, skip + limit)
        if label:
            _.hasLabel(label)
        if query:
            for k, v in query.items():
                _.has(k, v)
        return _

    def filter_edge(self, edge_id=None, label=None, query=None):
        """

        :param edge_id:
        :param label:
        :param query:
        :return:
        """
        query = {} if query is None else query
        _ = self.gremlin_client.g.E(edge_id) if edge_id else self.gremlin_client.g.E()
        if label:
            _.hasLabel(label)
        for k, v in query.items():
            _.has(k, v)
        return _

    @abc.abstractmethod
    def create(self, label=None, properties=None, **kwargs):
        pass

    @abc.abstractmethod
    def update(self, elem, properties=None):
        pass

    @abc.abstractmethod
    def _read_one(self, element_id):
        pass

    def read_one(self, element_id):
        return self._read_one(element_id)

    @abc.abstractmethod
    def _read_many(self, label=None, query=None, limit=None, skip=None):
        pass

    def read_many(self, label=None, query=None, limit=None, skip=None):
        return self._read_many(label=label, query=query, limit=limit, skip=skip)

    @abc.abstractmethod
    def _delete_one(self, element_id):
        pass

    def delete_one(self, element_id):
        return self._delete_one(element_id)

    @staticmethod
    def validate_filter_many_filters(label=None, query=None):
        if label is None and query is None:
            raise InvalidQueryArguments("Both label and query arguments cannot be none")
        pass

    @abc.abstractmethod
    def _delete_many(self, label=None, query=None):
        pass

    def delete_many(self, label=None, query=None):
        self.validate_filter_many_filters(label=label, query=query)
        return self._delete_many(label=label, query=query)

    @abc.abstractmethod
    def get_or_create(self, label=None, query=None):
        pass

    @staticmethod
    def drop(_):
        _.drop().iterate()
