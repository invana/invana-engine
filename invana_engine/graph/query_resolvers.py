#  Copyright 2021 Invana
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#  http:www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from invana_engine.data_types import NodeOrEdgeType, AnyField, NodeType, \
    QueryResponseData, EdgeType, getOrCreateNodeType
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT, DEFAULT_PAGINATION_SIZE
import graphene


# class RawQuerySchema(graphene.ObjectType):
#     get_vertices = graphene.Field(graphene.List(GrapheneVertexType),
#                                    label=String(),
#
#                                    query=JSONString(),
#                           limit=Int(default_value=default_pagination_size), skip=Int())
#
#     def resolve_get_vertex_model(self, info: graphene.ResolveInfo, label: str = None) -> LabelSchemaVertexType:
#         model = info.context['request'].app.state.graph.management.schema_reader.get_vertex_schema(label)
#         model.properties = model.properties_as_list()
#         return model
#


class GremlinGenericQuerySchema:
    execute_query = graphene.Field(QueryResponseData, timeout=graphene.Int(default_value=DEFAULT_QUERY_TIMEOUT),
                                   gremlin=graphene.String())

    get_vertices = graphene.Field(graphene.List(NodeType), filters=graphene.JSONString(),
                                  limit=graphene.Int(default_value=DEFAULT_PAGINATION_SIZE), skip=graphene.Int())
    get_or_create_vertex = graphene.Field(getOrCreateNodeType, label=graphene.String(),
                                          properties=graphene.JSONString())

    # get_or_create_edge = graphene.Field(EdgeType, label=graphene.String(), properties=graphene.JSONString())

    def resolve_execute_query(self, info: graphene.ResolveInfo, gremlin: str, timeout: int) -> any:
        response = info.context['request'].app.state.graph.execute_query(gremlin, timeout=timeout)
        return {"data": [d.to_json() if hasattr(d, "to_json") else d for d in response.data] if response.data else []}

    def resolve_get_vertices(self, info: graphene.ResolveInfo, filters: dict = None,
                             limit: int = DEFAULT_PAGINATION_SIZE, skip: int = 0):
        filters = {} if filters is None else filters
        data = info.context['request'].app.state.graph.vertex.search(
            limit=limit, skip=skip, **filters
        ).order_by('id').range(skip, limit).to_list()
        return [datum.to_json() for datum in data]

    def resolve_get_or_create_vertex(self, info: graphene.ResolveInfo, label: str = None,
                                     properties=None):
        _ = info.context['request'].app.state.graph.vertex.get_or_create(label, **properties)
        return dict(zip(['is_created', 'data'], [_[0], _[1].to_json()]))

    # def resolve_get_or_create_edge(self, info: graphene.ResolveInfo, label: str = None,
    #                                  properties: str = None):
    #     return info.context['request'].app.state.graph.edge.get_or_create(label, **properties)
