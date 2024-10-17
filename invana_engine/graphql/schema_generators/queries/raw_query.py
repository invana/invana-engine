import graphene
from invana_engine.graphql.data_types import QueryResponseData
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT

class ExecuteQueryType(graphene.ObjectType):
    _execute_query = graphene.Field(QueryResponseData, 
                                   timeout=graphene.Int(default_value=DEFAULT_QUERY_TIMEOUT),
                                   query=graphene.String(), 
                                   query_language=graphene.String(required=False))


    def resolve__execute_query(self, info, query, timeout, query_language=None):
        response = info.context['request'].app.state.graph.execute_query(query, timeout=timeout, 
                                                                         query_language=query_language)
        return {"data": [d.to_json() if hasattr(d, "to_json") else d for d in response.data] if response.data else []}
