import typing as T
if T.TYPE_CHECKING:
    from invana_engine.backends import GremlinBackend
from invana_engine.backends.base.queryset import SchemaQuerySetAbstract


class GremlinSchemaQuerySet(SchemaQuerySetAbstract):

    def __init__(self, backend: 'GremlinBackend'):
        super().__init__(backend)

    def get_schema(self, *args, **kwargs):
        return super().get_schema(*args, **kwargs)
    
    def get_node_schema(self, *args, **kwargs):
        return super().get_node_schema(*args, **kwargs)
    
    def get_edge_schema(self, *args, **kwargs):
        return super().get_edge_schema(*args, **kwargs) 