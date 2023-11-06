from invana_engine2.invana.gremlin.querysets.management import GremlinGraphManagementQuerySet
from .extras import JanusGraphExtrasQuerySet


class JanusGraphGraphManagementQuerySet(GremlinGraphManagementQuerySet):

    extras_cls = JanusGraphExtrasQuerySet
    