import abc
from .backend import BackendAbstract
import abc
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from .requestsets import QueryResultSetBase


class QuerySetAbstract(abc.ABC):

    def __init__(self, backend: BackendAbstract):
        self.backend = backend

 
class GenericQuerySetAbstract(QuerySetAbstract):

    @abc.abstractmethod
    def run_query(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def search_v(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def search_e(self, *args, **kwargs):
        pass


    @abc.abstractmethod
    def get_inv(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_outv(self, *args, **properties):
        pass

    @abc.abstractmethod
    def get_bothv(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_ine(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_oute(self, *args, **kwargs):
        pass
 
    @abc.abstractmethod
    def get_bothe(self, **kwargs):
        pass
 
    @abc.abstractmethod
    def search(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_node_by_id(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_edge_by_id(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_node_stats(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_edge_stats(self, *args, **kwargs):
        pass


class SchemaQuerySetAbstract(QuerySetAbstract):

    @abc.abstractmethod
    def get_schema(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_node_schema(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_edge_schema(self, *args, **kwargs):
        pass
