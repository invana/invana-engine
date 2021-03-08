import abc
from .core.exceptions import InvalidQueryArguments


class GremlinOperationBase:

    def __init__(self, gremlin_client=None):
        """

        :param gremlin_client: InvanaEngineClient instance
        """
        self.gremlin_client = gremlin_client

    @staticmethod
    def get_namespaced_label(label=None, namespace=None):
        return "{}/{}".format(namespace, label) if namespace else label

    @property
    def serializer(self):
        return self.gremlin_client.serializer


class CRUDOperationsBase(GremlinOperationBase, metaclass=abc.ABCMeta):

    def filter_vertex(self, vertex_id=None, label=None, namespace=None, query=None, limit=None, skip=None):
        """

        :param vertex_id:
        :param label:
        :param namespace:
        :param query:
        :param limit:
        :param skip:
        :return:
        """
        label = self.get_namespaced_label(label=label, namespace=namespace)
        query = {} if query is None else query
        _ = self.gremlin_client.g.V(vertex_id) if vertex_id else self.gremlin_client.g.V()
        if label:
            _.hasLabel(label)
        if query:
            for k, v in query.items():
                _.has(k, v)
        if limit is not None and skip is not None:  # TODO - pagination fixes needed
            _.range(skip, skip + limit)
        return _

    def filter_edge(self, edge_id=None, label=None, namespace=None, query=None, limit=None, skip=None):
        """

        :param edge_id:
        :param label:
        :param namespace:
        :param query:
        :param limit:
        :param skip:
        :return:
        """
        label = self.get_namespaced_label(label=label, namespace=namespace)
        query = {} if query is None else query
        _ = self.gremlin_client.g.E(edge_id) if edge_id else self.gremlin_client.g.E()
        if label:
            _.hasLabel(label)
        for k, v in query.items():
            _.has(k, v)
        if limit is not None and skip is not None:  # TODO - pagination fixes needed
            _.range(skip, skip + limit)

        return _

    @abc.abstractmethod
    def create(self, label=None, namespace=None, properties=None, **kwargs):
        pass

    @abc.abstractmethod
    def update(self, elem_id, properties=None):
        pass

    @abc.abstractmethod
    def _read_one(self, element_id):
        pass

    def read_one(self, element_id):
        return self._read_one(element_id)

    @abc.abstractmethod
    def _read_many(self, label=None, namespace=None, query=None, limit=None, skip=None):
        pass

    def read_many(self, label=None, namespace=None, query=None, limit=None, skip=None):
        return self._read_many(label=label, namespace=namespace, query=query, limit=limit, skip=skip)

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
    def _delete_many(self, label=None, namespace=None, query=None):
        pass

    def delete_many(self, label=None, namespace=None, query=None):
        self.validate_filter_many_filters(label=label, query=query)
        return self._delete_many(label=label, namespace=namespace, query=query)

    @abc.abstractmethod
    def get_or_create(self, label=None, namespace=None, properties=None):
        pass

    @staticmethod
    def drop(_):
        _.drop().iterate()
