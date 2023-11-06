import graphene
from ..utils import get_client_info, get_host
import socket


class BackendInfoType(graphene.ObjectType):
    url = graphene.String()
    name = graphene.String()
    backend_class = graphene.String() 
    # host_name = graphene.String()
    # host_ip_address = graphene.String()
    # features = graphene.Field(FeaturesInfo)

    # def resolve_features(self, info):
    #     features_data = info.context['request'].app.state.graph.connector.get_features().data
    #     data = {}
    #     for k, v in features_data.items():
    #         data[snake_case_to_camel_case(k)] = v
    #     return data

    # def resolve__get_client_info(self, info):
    #     result = get_client_info()
    #     result['gremlin_host'] = get_host(info.context['request'].app.state.graph.connector.connection_uri)
    #     result['gremlin_traversal_source'] = info.context['request'].app.state.graph.connector.traversal_source
    #     return result

class ClientInfoType(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="World"))
    host = graphene.String()
    host_ip_address = graphene.String()
    backend = graphene.Field(BackendInfoType)

    def resolve_hello(self, info, name):
        return name
    
    def resolve_host(self, info):
        return socket.gethostname()
 
    def resolve_host_ip_address(self, info):
        return socket.gethostbyname(socket.gethostname())
 
