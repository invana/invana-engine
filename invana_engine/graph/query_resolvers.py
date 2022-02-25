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
from .types import NodeOrEdgeType
import graphene


# class RawQuerySchema(graphene.ObjectType):
#     filter_vertex = graphene.Field(graphene.List(GrapheneVertexType),
#                                    label=String(),
#
#                                    query=JSONString(),
#                           limit=Int(default_value=default_pagination_size), skip=Int())
#
#     def resolve_get_vertex_model(self, info: graphene.ResolveInfo, label: str = None) -> ModelVertexLabel:
#         model = info.context['request'].app.state.graph.management.schema_reader.get_vertex_schema(label)
#         model.properties = model.properties_as_list()
#         return model
#


class GremlinGenericQuerySchema:
    raw_query = graphene.Field(graphene.List(NodeOrEdgeType), timeout=graphene.Int(), gremlin=graphene.String())

    def resolve_raw_query(self, info: graphene.ResolveInfo, gremlin: str, timeout: int) -> any:
        data = info.context['request'].app.state.graph.execute_query(gremlin, timeout=timeout).data
        return [d.to_json() for d in data]
