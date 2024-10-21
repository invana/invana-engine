import graphene
from ...data_types import QueryResponseData
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT

class RunQueryObjectType(graphene.ObjectType):
    _run_query = graphene.Field(
                        QueryResponseData, 
                        timeout=graphene.Int(
                            default_value=DEFAULT_QUERY_TIMEOUT,
                            description="time in milliseconds before which query shall timeout"
                        ),
                        query=graphene.String(), 
                        query_language=graphene.String(required=False))


    def resolve__run_query(self, info, query, timeout, query_language=None):
        response = info.context['request'].app.state.graph.run_query(query, timeout=timeout, 
                                                                         query_language=query_language)
        return {"data": [d.to_json() if hasattr(d, "to_json") else d for d in response.data] if response.data else []}
