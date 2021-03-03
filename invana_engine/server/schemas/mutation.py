from graphene import ObjectType, String, Field, JSONString, ResolveInfo, Int, NonNull, List
from ..types.element import GrapheneVertexType, GrapheneEdgeType, AnyField


class GremlinVertexMutationSchema:
    create_vertex = Field(GrapheneVertexType, label=String(required=True), namespace=String(),
                          properties=JSONString(required=True))
    update_vertex_by_id = Field(GrapheneVertexType, id=AnyField(required=True), properties=JSONString(required=True))
    remove_vertex_by_id = String(id=AnyField(required=True))
    remove_vertices = String(label=String(), namespace=String(), query=JSONString())

    def resolve_create_vertex(self, info: ResolveInfo, label: str, namespace: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.vertex.create(
            label=label, namespace=namespace, properties=properties)
        return data.__dict__() if data else None

    def resolve_update_vertex_by_id(self, info: ResolveInfo, id: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.vertex.update(id, properties=properties)
        return data.__dict__() if data else None

    def resolve_remove_vertex_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.vertex.delete_one(id)
        return data.__dict__() if data else None

    def resolve_remove_vertices(self, info: ResolveInfo, label: str = None, namespace: str = None, query: str = None):
        info.context['request'].app.state.gremlin_client.vertex.delete_many(label=label,
                                                                            namespace=namespace, query=query)
        return None



class GremlinEdgeMutationSchema:
    create_edge = Field(GrapheneEdgeType,
                        inv=String(required=True),
                        outv=String(required=True),
                        label=String(required=True),
                        name=String(),
                        properties=JSONString())
    update_edge_by_id = Field(GrapheneEdgeType, id=AnyField(required=True), properties=JSONString(required=True))
    remove_edge_by_id = String(id=AnyField(required=True))
    remove_edges = String(label=String(), namespace=String(), query=JSONString())

    def resolve_create_edge(self, info: ResolveInfo, label: str, namespace: str, properties: str, inv: str, outv: str):
        return info.context['request'].app.state.gremlin_client.edge.create(
            outv=outv, inv=inv, label=label, namespace=namespace, properties=properties
        )

    def resolve_update_edge_by_id(self, info: ResolveInfo, id: str, properties: str):
        data = info.context['request'].app.state.gremlin_client.edge.update(id, properties=properties)
        return data.__dict__() if data else None

    def resolve_remove_edge_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.gremlin_client.edge.delete_one(id)
        return data.__dict__() if data else None

    def resolve_remove_edges(self, info: ResolveInfo, label: str = None, namespace: str = None, query: str = None):
        info.context['request'].app.state.gremlin_client.edge.delete_many(label=label,
                                                                          namespace=namespace, query=query)
        return None



class GremlinMutation(ObjectType, GremlinEdgeMutationSchema, GremlinVertexMutationSchema):
    pass
