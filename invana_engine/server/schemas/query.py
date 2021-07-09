#  Copyright 2020 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from graphene import ObjectType, String, Field, JSONString, ResolveInfo, Int, List
from ..types.element import GrapheneVertexType


class VertexSchema:
    get_or_create_vertex = Field(GrapheneVertexType, label=String(), properties=JSONString())

    def resolve_get_or_create_vertex(self, info: ResolveInfo, label: str = None, properties: str = None):
        return info.context['request'].app.state.gremlin_client.vertex.get_or_create(
            label=label, properties=properties)


class QuerySchema(ObjectType, VertexSchema):
    pass
