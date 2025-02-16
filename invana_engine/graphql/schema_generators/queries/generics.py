import graphene
from ...data_types import QueryResponseData
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT
from invana_engine.graph import InvanaGraph
from invana_engine.graphql.data_types import NodeType, EdgeType
from invana_engine.settings import DEFAULT_PAGINATION_SIZE


class GenericQueriesObjectType(graphene.ObjectType):


    get_vertices = graphene.Field(graphene.List(NodeType),
                                  filters=graphene.JSONString(),
                                  order_by=graphene.String(),
                                  limit=graphene.Int(default_value=DEFAULT_PAGINATION_SIZE),
                                  skip=graphene.Int())
    get_edges = graphene.Field(graphene.List(EdgeType),
                               filters=graphene.JSONString(),
                               get_vertex_properties=graphene.Boolean(default_value=False),
                               limit=graphene.Int(default_value=DEFAULT_PAGINATION_SIZE),
                               order_by=graphene.String(),
                               skip=graphene.Int())
    

    def resolve_get_vertices(self, info: graphene.ResolveInfo, filters: dict = None,
                             order_by: str = None,
                             limit: int = DEFAULT_PAGINATION_SIZE, skip: int = 0):
        filters = {} if filters is None else filters
        graph: InvanaGraph = info.context['request'].app.state.graph             
        _ = graph.backend.objects.search(
            limit=limit, skip=skip, **filters
        )
        if order_by:
            _.order_by(order_by)
        data = _.range(skip, limit).to_list()
        return [datum.to_json() for datum in data]

    def resolve_get_edges(self, info: graphene.ResolveInfo, filters: dict = None,
                          order_by: str = None, get_vertex_properties: bool = None,
                          limit: int = DEFAULT_PAGINATION_SIZE, skip: int = 0):
        filters = {} if filters is None else filters
        _ = info.context['request'].app.state.graph.edge.search(
            limit=limit, skip=skip, **filters
        )
        if order_by:
            _.order_by(order_by)
        data = _.range(skip, limit).to_list()
        if get_vertex_properties is True:
            data = get_vertex_properties_of_edges(data, info.context['request'].app.state.graph)
        __ = [datum.to_json() for datum in data]
        return __
