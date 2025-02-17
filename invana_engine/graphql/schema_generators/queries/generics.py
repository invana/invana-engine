import graphene
from invana_engine.graph import InvanaGraph
from invana_engine.graphql.data_types import NodeType, EdgeType, NodesAndEdgesObjectType
from invana_engine.settings import DEFAULT_PAGINATION_SIZE
from invana_engine.backends.gremlin.utils import get_vertex_properties_of_edges, get_neighbor_nodes_and_edges_of_nodes


class GenericQueriesObjectType(graphene.ObjectType):


    _search_nodes = graphene.Field( NodesAndEdgesObjectType,
                                  filters=graphene.JSONString(),
                                #   order_by=graphene.String(),
                                    get_neighbors= graphene.Boolean(default_value=False),  
                                  limit=graphene.Int(default_value=DEFAULT_PAGINATION_SIZE),
                                  skip=graphene.Int())
    _search_edges = graphene.Field(NodesAndEdgesObjectType,
                               filters=graphene.JSONString(),
                                get_neighbors= graphene.Boolean(default_value=False),  
                               limit=graphene.Int(default_value=DEFAULT_PAGINATION_SIZE),
                               order_by=graphene.String(),
                               skip=graphene.Int())
    

    def resolve__search_nodes(self, info: graphene.ResolveInfo, 
                            filters: dict = None,
                            get_neighbors: int = None,
                            # order_by: str = None,
                            limit: int = DEFAULT_PAGINATION_SIZE, skip: int = 0):
        filters = {} if filters is None else filters
        graph: InvanaGraph = info.context['request'].app.state.graph             
        _ = graph.backend.objects.search_nodes(
            limit=limit, skip=skip, get_neighbors=get_neighbors, **filters
        )
        """

        # order not working 
        if order_by:
            _.order_by(order_by)
        # skipping  -  _.range(skip, limit)
        # it is failing because of the range method in the GremlinQueryResultSet
        """

        # if get_neighbors:
        #     data = _.to_list()

        #     # for __ in range(get_neighbors):
        #     #     _._as('edges').bothV()._as('vertex')

        #     # data = _.select('edge', 'vertex').to_list()  
        #     return get_neighbor_nodes_and_edges_of_nodes(data, graph)
        
        return {
            "nodes" : [datum.to_json() for datum in _.to_list()], 
            "edges": []
        }

    def resolve__search_edges(self, info: graphene.ResolveInfo, filters: dict = None,
                        #   order_by: str = None, 
                          get_neighbors: int = None,
                          limit: int = DEFAULT_PAGINATION_SIZE, skip: int = 0):
        filters = {} if filters is None else filters
        graph: InvanaGraph = info.context['request'].app.state.graph             
        _ = graph.backend.objects.search_edges(
            limit=limit, skip=skip, **filters
        )

        """
        # order not working 
        if order_by:
            _.order_by(order_by)

        # skipping  -  _.range(skip, limit)
        # it is failing because of the range method in the GremlinQueryResultSet
        """
        data = _.to_list()
        # if get_neighbors :
        #     return get_vertex_properties_of_edges(data, graph)

        if get_neighbors:
            # data = _.to_list()

            # for __ in range(get_neighbors):
            #     _._as('edges').bothV()._as('vertex')

            # data = _.select('edge', 'vertex').to_list()  
            return get_vertex_properties_of_edges(data, graph)
 
        return {
            "nodes": [], 
            "edges":  [datum.to_json() for datum in data]
        }
