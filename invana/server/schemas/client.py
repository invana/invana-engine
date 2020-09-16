import graphene
from ..types.gremlin import GremlinClientInfo
from ..utils import get_host, get_client_info


class GenericClientInfoSchema:
    hello = graphene.String(name=graphene.String(default_value="World"))
    get_client_info = graphene.Field(GremlinClientInfo)

    def resolve_hello(self, info: graphene.ResolveInfo, name: any) -> str:
        return "Hello " + name

    def resolve_get_client_info(self, info: graphene.ResolveInfo):
        result = get_client_info()
        result['gremlin_host'] = get_host(info.context['request'].app.state.gremlin_client.gremlin_server_url)
        return result
