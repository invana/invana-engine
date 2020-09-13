from graphene import ObjectType, String, Field, JSONString, ResolveInfo, Int, NonNull
from ..utils import get_host, get_client_info
from ..types.element import GraphElement, GenericJSONField

from ..types.gremlin import GremlinClientInfo


class Gremlin(ObjectType):
    hello = String(name=String(default_value="World"))
    raw_query = String(gremlin=String())
    create_vertex = String(label=String(), properties=JSONString())
    get_vertex_by_id = Field(GraphElement, id=String())
    update_vertex_by_id = String(id=String(), properties=JSONString())
    remove_vertex_by_id = String(id=String())
    filter_vertex = String(label=String(), query=JSONString(), limit=Int(), skip=Int())
    get_client_info = Field(GremlinClientInfo)

    def resolve_hello(self, info: ResolveInfo, name: any) -> str:
        return "Hello " + name

    def resolve_raw_query(self, info: ResolveInfo, gremlin: str) -> any:
        return info.context['request'].app.state.gremlin_client.execute_query(gremlin)

    def resolve_get_client_info(self, info: ResolveInfo):
        result = get_client_info()
        result['gremlin_host'] = get_host(info.context['request'].app.state.gremlin_client.gremlin_server_url)
        return result

    def resolve_create_vertex(self, info: ResolveInfo, label: str, properties: str):
        return info.context['request'].app.state.gremlin_client.vertex.create(label=label, properties=properties)

    def resolve_update_vertex_by_id(self, info: ResolveInfo, id: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.vertex.update(id, properties=properties)
        return data.__dict__() if data else None

    def resolve_get_vertex_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.vertex.read_one(id)
        return data.__dict__() if data else None

    def resolve_remove_vertex_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.vertex.delete_one(id)
        return data.__dict__() if data else None

    def resolve_filter_vertex(self, info: ResolveInfo, label: str, query: str, limit: int, skip: int):
        data = info.context['request'].app.state.gremlin_client.vertex.read_many(
            label=label,
            query=query,
            limit=limit,
            skip=skip
        )
        return data.__dict__() if data else None
