from .base import GremlinQuerySetBase
from invana_engine.invana.base.querysets.graph import EdgeCRUDQuerySetBase
from ..resultsets import GremlinQueryResultSet
from ..traversal.traversal import __
import abc


class GremlinEdgeQuerySet(GremlinQuerySetBase, EdgeCRUDQuerySetBase, abc.ABC):

    def create(self, label, from_, to_, **properties) -> GremlinQueryResultSet:
        return GremlinQueryResultSet(self.connector.g.create_edge(label, from_, to_, **properties))

    def search(self, **search_kwarg) -> GremlinQueryResultSet:
        return GremlinQueryResultSet(self.connector.g.E().search(**search_kwarg))

    def delete(self, **search_kwarg):
        return self.search(**search_kwarg).drop()

    def get_or_create(self, label, from_, to_, **properties):
        elem = self.connector.g.V(from_).outE().search(has__label=label, **properties).where(
            __.inV().hasId(to_)).elementMap().toList()
        created = False
        if elem.__len__() == 0:
            elem = self.create(label, from_, to_, **properties).get_traversal().elementMap().toList()
            created = True
        return created, elem[0] if elem.__len__() > 0 else None

    def get_or_none(self, label, from_, to_, **properties):
        elem = self.connector.g.V(from_).outE().search(has__label=label, **properties).where(
            __.inV().hasId(to_)).elementMap().toList()
        return elem[0] if elem.__len__() > 0 else None

    def get_by_id(self, relationId):
        return self.connector.g.E(relationId).next()

    def bulk_write(self, *args, **kwargs):
        # TODO - implement this
        raise NotImplementedError()

