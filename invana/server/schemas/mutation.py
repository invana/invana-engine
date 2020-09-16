from graphene import ObjectType, String, Field, JSONString, ResolveInfo, Int, NonNull, List
from ..types.element import GrapheneVertexType, GrapheneEdgeType

default_pagination_size = 10


class GremlinVertexMutationSchema:
    create_vertex = Field(GrapheneVertexType, label=String(required=True), properties=JSONString(required=True))
    update_vertex_by_id = Field(GrapheneVertexType, id=String(required=True), properties=JSONString(required=True))
    remove_vertex_by_id = String(id=String(required=True))
    remove_vertices = String(label=String(), query=JSONString())

    def resolve_create_vertex(self, info: ResolveInfo, label: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.vertex.create(label=label, properties=properties)
        return data.__dict__() if data else None

    def resolve_update_vertex_by_id(self, info: ResolveInfo, id: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.vertex.update(id, properties=properties)
        return data.__dict__() if data else None

    def resolve_remove_vertex_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.vertex.delete_one(id)
        return data.__dict__() if data else None

    def resolve_remove_vertices(self, info: ResolveInfo, label: str = None, query: str = None):
        info.context['request'].app.state.gremlin_client.vertex.delete_many(label=label, query=query)
        return None


class GremlinEdgeMutationSchema:
    create_edge = Field(GrapheneEdgeType,
                        inv=String(required=True),
                        outv=String(required=True),
                        label=String(required=True),
                        properties=JSONString())
    update_edge_by_id = Field(GrapheneEdgeType, id=String(required=True), properties=JSONString(required=True))
    remove_edge_by_id = String(id=String(required=True))

    def resolve_create_edge(self, info: ResolveInfo, label: str, properties: str, inv: str, outv: str):
        return info.context['request'].app.state.gremlin_client.edge.create(
            outv=outv, inv=inv, label=label, properties=properties
        )

    def resolve_update_edge_by_id(self, info: ResolveInfo, id: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.edge.update(id, properties=properties)
        return data.__dict__() if data else None

    def resolve_remove_edge_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.edge.delete_one(id)
        return data.__dict__() if data else None


class GremlinMutation(ObjectType, GremlinEdgeMutationSchema, GremlinVertexMutationSchema):
    pass
