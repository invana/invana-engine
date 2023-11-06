from graphene import ObjectType, String, Field, JSONString, ResolveInfo, Int, NonNull, List

from invana_engine2.data_types import AnyField, NodeType, EdgeType


class VertexMutationSchema(ObjectType):
    create_vertex = Field(NodeType, label=String(required=True), namespace=String(),
                          properties=JSONString(required=True))
    update_vertex_by_id = Field(NodeType, id=AnyField(required=True), properties=JSONString(required=True))
    remove_vertex_by_id = String(id=AnyField(required=True))
    remove_vertices = String(filters=JSONString())

    def resolve_create_vertex(self, info: ResolveInfo, label: str, namespace: str, properties):
        data = info.context['request'].app.state.graph.vertex.create(
            label=label, **properties)
        return data.__dict__() if data else None

    def resolve_update_vertex_by_id(self, info: ResolveInfo, id: str, properties: dict):
        info.context['request'].app.state.graph.vertex.search(has__id=id).update(**properties)
        _ = info.context['request'].app.state.graph.vertex.search(has__id=id).to_list()
        return _[0].to_json() if _ and _.__len__() > 0 else None

    def resolve_remove_vertex_by_id(self, info: ResolveInfo, id: str):
        data = info.context['request'].app.state.graph.vertex.delete(has__id=id)
        return data.__dict__() if data else None

    def resolve_remove_vertices(self, info: ResolveInfo, filters: dict = None):
        info.context['request'].app.state.graph.vertex.edlete(**filters)
        return None


# class GremlinEdgeMutationSchema(ObjectType):
#     create_edge = Field(EdgeType,
#                         inv=String(required=True),
#                         outv=String(required=True),
#                         label=String(required=True),
#                         name=String(),
#                         properties=JSONString())
#     update_edge_by_id = Field(EdgeType, id=AnyField(required=True), properties=JSONString(required=True))
#     remove_edge_by_id = String(id=AnyField(required=True))
#     remove_edges = String(label=String(), namespace=String(), query=JSONString())
#
#     def resolve_create_edge(self, info: ResolveInfo, label: str, namespace: str, properties: str, inv: str, outv: str):
#         return info.context['request'].app.state.graph.edge.create(
#             outv=outv, inv=inv, label=label, **properties
#         )
#
#     def resolve_update_edge_by_id(self, info: ResolveInfo, id: str, properties: str):
#         data = info.context['request'].app.state.graph.edge.update(id, properties=properties)
#         return data.__dict__() if data else None
#
#     def resolve_remove_edge_by_id(self, info: ResolveInfo, id: str):
#         data = info.context['request'].app.state.graph.edge.delete_one(id)
#         return data.__dict__() if data else None
#
#     def resolve_remove_edges(self, info: ResolveInfo, label: str = None, namespace: str = None, query: str = None):
#         info.context['request'].app.state.graph.edge.delete_many(label=label,
#                                                                  namespace=namespace, query=query)
#         return None


# class MutationSchema(GremlinEdgeMutationSchema, VertexMutationSchema):
class MutationSchema(VertexMutationSchema):
    pass
