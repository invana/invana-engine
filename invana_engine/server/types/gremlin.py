from graphene import ObjectType, String, Int
from ..utils import get_host, get_client_info


class GremlinClientInfo(ObjectType):
    gremlin_host = String()
    gremlin_traversal_source = String()
    host_name = String()
    ip_address = String()

    def resolve_gremlin_host(self, info):
        return get_host(info.context['request'].app.state.gremlin_client.gremlin_server_url)

    def resolve_gremlin_traversal_source(self, info):
        return info.context['request'].app.state.gremlin_client.gremlin_traversal_source

    def resolve_host_name(self, info):
        return get_client_info()['host_name']

    def resolve_ip_address(self, info):
        return get_client_info()['ip_address']


class LabelStats(ObjectType):
    label = String()
    count = Int()
