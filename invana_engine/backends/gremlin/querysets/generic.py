import typing as T
if T.TYPE_CHECKING:
    from invana_engine.backends import GremlinBackend
from invana_engine.backends.base.queryset import GenericQuerySetAbstract


class GremlinQuerySet(GenericQuerySetAbstract):

    def __init__(self, backend: 'GremlinBackend'):
        super().__init__(backend)

    
    def run_query(self, *args, **kwargs):
        return self.backend.run_query(*args, **kwargs)

    
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