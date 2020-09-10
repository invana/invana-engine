from graphene import ObjectType, JSONString, String, Field
import socket
from .utils import get_host

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


class GremlinClientInfo(ObjectType):
    gremlin_host = String()
    hostname = String()
    ip_address = String()


class GraphElement(ObjectType):
    id = String()
    type = String()
    label = String()
    properties = JSONString()


class GremlinQuery(ObjectType):
    hello = String(name=String(default_value="World"))
    vertex_create = String(label=String(), properties=JSONString())
    vertex_get = Field(GraphElement, id=String())
    get_client_info = Field(GremlinClientInfo)

    def resolve_hello(self, info, name: any) -> str:
        return "Hello " + name

    def resolve_get_client_info(self, info):
        return {
            "gremlin_host": get_host(info.context['request'].app.state.gremlin_client.gremlin_server_url),
            "hostname": hostname,
            "ip_address": ip_address
        }

    def resolve_vertex_create(self, info, label, properties):
        return info.context['request'].app.state.gremlin_client.vertex.create(label=label, properties=properties)

    def resolve_vertex_get(self, info, id):
        data = info.context['request'].app.state.gremlin_client.vertex.read_one(element_id=id)
        return data.__dict__()
