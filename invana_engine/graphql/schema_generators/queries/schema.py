import graphene
from ...data_types import QueryResponseObjectType
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT
from invana_engine.graph import InvanaGraph

class SchemaQueryObjectType(graphene.ObjectType):

    _get_schema = graphene.Field(
                        QueryResponseObjectType, 
                        timeout=graphene.Int(
                            default_value=DEFAULT_QUERY_TIMEOUT,
                            description="time in milliseconds before which query shall timeout"
                        ),
                        query=graphene.String(), 
                        query_language=graphene.String(required=False))


    def resolve__run_query(self, info, query, timeout, query_language=None):
        graph: InvanaGraph = info.context['request'].app.state.graph
        response = graph.backend.objects.run_query(
                query, 
                timeout=timeout, 
                query_language=query_language
            )
        return {"data": [d.to_json() if hasattr(d, "to_json") else d for d in response.data]
                 if response.data else []}
