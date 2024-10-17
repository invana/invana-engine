import graphene
from invana_engine.graphql.utils import get_client_info, get_host
import socket
from invana_engine.settings import __VERSION__


class BackendBasicInfoType(graphene.ObjectType):
    connection_uri = graphene.String()
    backend_class = graphene.String()
    is_readonly = graphene.Boolean()
    default_query_language = graphene.String()
    supported_query_languages = graphene.List(graphene.String)

class ClientInfoType(graphene.ObjectType):
    host = graphene.String()
    host_ip_address = graphene.String()
    backend = graphene.Field(BackendBasicInfoType)


class BasicInfoType(graphene.ObjectType):
    _hello = graphene.String( )
    _version = graphene.String()
    _client = graphene.Field(ClientInfoType)

    def resolve__version(self, info: graphene.ResolveInfo) -> str:
        return __VERSION__

    def resolve__hello(self, info):
        request = info.context["request"]
        user_agent = request.headers.get("user-agent", "guest")
        return "Hello, %s!" % user_agent
        
    def resolve__client(self, info):
        # return get_client_info()
        data = {
            "host": info.context['request'].base_url._url.rstrip("/"),
            "host_ip_address": info.context['request'].base_url.netloc,
        }
        try:
            data['backend'] = info.context['request'].app.state.graph.backend.get_basic_info()
        except:
            data['backend'] = "NA"
        return data