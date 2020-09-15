from graphene import ObjectType, String, Field, JSONString, ResolveInfo, Int, NonNull, List
from ..utils import get_host, get_client_info
from ..types.element import GrapheneVertexType, GrapheneEdgeType
from ..types.gremlin import GremlinClientInfo

default_pagination_size = 10


class GenericSchema:
    hello = String(name=String(default_value="World"))
    get_client_info = Field(GremlinClientInfo)

    def resolve_hello(self, info: ResolveInfo, name: any) -> str:
        return "Hello " + name

    def resolve_get_client_info(self, info: ResolveInfo):
        result = get_client_info()
        result['gremlin_host'] = get_host(info.context['request'].app.state.gremlin_client.gremlin_server_url)
        return result


class VertexGremlinSchema:
    create_vertex = Field(GrapheneVertexType, label=String(required=True), properties=JSONString(required=True))
    get_vertex_by_id = Field(GrapheneVertexType, id=String(required=True))
    update_vertex_by_id = Field(GrapheneVertexType, id=String(required=True), properties=JSONString(required=True))
    remove_vertex_by_id = String(id=String(required=True))
    filter_vertex = Field(List(GrapheneVertexType), label=String(), query=JSONString(),
                          limit=Int(default_value=default_pagination_size), skip=Int())
    get_in_edge_vertices = Field(List(GrapheneVertexType), id=String(required=True), label=String(), query=JSONString(),
                                 limit=Int(default_value=default_pagination_size), skip=Int())
    get_out_edge_vertices = Field(List(GrapheneVertexType), id=String(required=True), label=String(), query=JSONString(),
                                 limit=Int(default_value=default_pagination_size), skip=Int())

    remove_vertices = String(label=String(), query=JSONString())

    def resolve_create_vertex(self, info: ResolveInfo, label: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.vertex.create(label=label, properties=properties)
        return data.__dict__() if data else None

    def resolve_update_vertex_by_id(self, info: ResolveInfo, id: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.vertex.update(id, properties=properties)
        return data.__dict__() if data else None

    def resolve_get_vertex_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.vertex.read_one(id)
        return data.__dict__() if data else None

    def resolve_remove_vertex_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.vertex.delete_one(id)
        return data.__dict__() if data else None

    def resolve_remove_vertices(self, info: ResolveInfo, label: str = None, query: str = None):
        info.context['request'].app.state.gremlin_client.vertex.delete_many(label=label, query=query)
        return None

    def resolve_filter_vertex(self, info: ResolveInfo, label: str = None, query: str = None,
                              limit: int = default_pagination_size, skip: int = 0):
        data = info.context['request'].app.state.gremlin_client.vertex.read_many(
            label=label, query=query, limit=limit, skip=skip
        )
        return [datum.__dict__() for datum in data]

    def resolve_get_in_edge_vertices(self, info: ResolveInfo,
                                     id: str = None, label: str = None, query: str = None,
                                     limit: int = default_pagination_size, skip: int = 0):
        data = info.context['request'].app.state.gremlin_client.vertex.read_in_edge_vertices(
            id, label=label, query=query, limit=limit, skip=skip
        )
        return [datum.__dict__() for datum in data]

    def resolve_get_out_edge_vertices(self, info: ResolveInfo,
                                      id: str = None, label: str = None, query: str = None,
                                      limit: int = default_pagination_size, skip: int = 0):
        data = info.context['request'].app.state.gremlin_client.vertex.read_out_edge_vertices(
            id, label=label, query=query, limit=limit, skip=skip
        )
        return [datum.__dict__() for datum in data]


class EdgeGremlinSchema:
    create_edge = Field(GrapheneEdgeType,
                        inv=String(required=True),
                        outv=String(required=True),
                        label=String(required=True),
                        properties=JSONString())
    get_edge_by_id = Field(GrapheneEdgeType, id=String(required=True))
    update_edge_by_id = Field(GrapheneEdgeType, id=String(required=True), properties=JSONString(required=True))
    remove_edge_by_id = String(id=String(required=True))
    filter_edge = Field(List(GrapheneEdgeType), label=String(), query=JSONString(),
                        limit=Int(default_value=default_pagination_size), skip=Int())

    def resolve_create_edge(self, info: ResolveInfo, label: str, properties: str, inv: str, outv: str):
        return info.context['request'].app.state.gremlin_client.edge.create(
            outv=outv, inv=inv, label=label, properties=properties
        )

    def resolve_get_edge_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.edge.read_one(id)
        return data.__dict__() if data else None

    def resolve_update_edge_by_id(self, info: ResolveInfo, id: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.edge.update(id, properties=properties)
        return data.__dict__() if data else None

    def resolve_remove_edge_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.edge.delete_one(id)
        return data.__dict__() if data else None

    def resolve_filter_edge(self, info: ResolveInfo, label: str = None, query: str = None,
                            limit: int = default_pagination_size, skip: int = 0):
        data = info.context['request'].app.state.gremlin_client.edge.read_many(
            label=label, query=query, limit=limit, skip=skip
        )
        return [datum.__dict__() for datum in data]


class Gremlin(ObjectType, EdgeGremlinSchema, VertexGremlinSchema, GenericSchema):
    raw_query = String(gremlin=String())

    def resolve_raw_query(self, info: ResolveInfo, gremlin: str) -> any:
        return info.context['request'].app.state.gremlin_client.execute_query(gremlin)
