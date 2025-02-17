import typing as T
if T.TYPE_CHECKING:
    from invana_engine.backends import GremlinBackend
from invana_engine.backends.base.queryset import GenericQuerySetAbstract
from ..resultset import GremlinQueryResultSet
from invana_engine.settings import DEFAULT_PAGINATION_SIZE


class GremlinQuerySet(GenericQuerySetAbstract):

    def __init__(self, backend: 'GremlinBackend'):
        super().__init__(backend)

    def run_query(self, *args, **kwargs):
        return self.backend.run_query(*args, **kwargs)

    # order_by:str= None, limit:int = DEFAULT_PAGINATION_SIZE, skip: int=0,
    def search_nodes(self, get_neighbors=None, **search_kwarg) -> GremlinQueryResultSet:
        traversal = self.backend.g.V().search(**search_kwarg)
        #._as('nodes').bothE()._as('edges').bothV()._as('neighbor_nodes')
        #print("traversal", traversal)
        # traversal._as('nodes').bothE()._as('edges').bothV()._as('neighbor_nodes')

        return GremlinQueryResultSet(traversal)

    def search_edges(self, **search_kwarg) -> GremlinQueryResultSet:
        return GremlinQueryResultSet(self.backend.g.E().search(**search_kwarg))
    
    def get_inv(self, **kwargs):
        pass
    
    def get_outv(self, *args, **properties):
        pass

    
    def get_bothv(self, **kwargs):
        pass

    
    def get_ine(self, *args, **kwargs):
        pass

    
    def get_oute(self, *args, **kwargs):
        pass

    
    def get_bothe(self, **kwargs):
        pass

    
    def search(self, *args, **kwargs):
        pass

    
    def get_node_by_id(self, *args, **kwargs):
        pass

    
    def get_edge_by_id(self, *args, **kwargs):
        pass

    
    def get_node_stats(self, *args, **kwargs):
        pass

    
    def get_edge_stats(self, *args, **kwargs):
        pass