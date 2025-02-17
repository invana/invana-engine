import graphene
from invana_engine.graph import InvanaGraph
from invana_engine.graphql.data_types import NodeType, EdgeType
from invana_engine.settings import DEFAULT_PAGINATION_SIZE
from invana_engine.backends.gremlin.utils import get_vertex_properties_of_edges


class GenericQueriesObjectType(graphene.ObjectType):


    _search_v = graphene.Field(graphene.List(NodeType),
                                  filters=graphene.JSONString(),
                                  order_by=graphene.String(),
                                  limit=graphene.Int(default_value=DEFAULT_PAGINATION_SIZE),
                                  skip=graphene.Int())
    _search_e = graphene.Field(graphene.List(EdgeType),
                               filters=graphene.JSONString(),
                               get_vertex_properties=graphene.Boolean(default_value=False),
                               limit=graphene.Int(default_value=DEFAULT_PAGINATION_SIZE),
                               order_by=graphene.String(),
                               skip=graphene.Int())
    

    def resolve__search_v(self, info: graphene.ResolveInfo, 
                            filters: dict = None,
                            order_by: str = None,
                            limit: int = DEFAULT_PAGINATION_SIZE, skip: int = 0):
        filters = {} if filters is None else filters
        graph: InvanaGraph = info.context['request'].app.state.graph             
        _ = graph.backend.objects.search_v(
            limit=limit, skip=skip, **filters
        )
        if order_by:
            _.order_by(order_by)
        """
        # skipping  -  _.range(skip, limit)
        # it is failing because of the range method in the GremlinQueryResultSet
        """
        data = _.to_list()
        return [datum.to_json() for datum in data]

    def resolve__search_e(self, info: graphene.ResolveInfo, filters: dict = None,
                          order_by: str = None, get_vertex_properties: bool = None,
                          limit: int = DEFAULT_PAGINATION_SIZE, skip: int = 0):
        filters = {} if filters is None else filters
        graph: InvanaGraph = info.context['request'].app.state.graph             
        _ = graph.backend.objects.search_e(
            limit=limit, skip=skip, **filters
        )
        if order_by:
            _.order_by(order_by)
        """
        # skipping  -  _.range(skip, limit)
        # it is failing because of the range method in the GremlinQueryResultSet
        """
        data = _.to_list()
        if get_vertex_properties is True:
            data = get_vertex_properties_of_edges(data, graph)
        return [datum.to_json() for datum in data]
