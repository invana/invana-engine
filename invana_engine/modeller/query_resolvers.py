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
from ..utils import get_host, get_client_info
from invana_engine.types import ModelEdgeLabel, ModelVertexLabel
import graphene


class GremlinClientInfo(graphene.ObjectType):
    gremlin_host = graphene.String()
    gremlin_traversal_source = graphene.String()
    host_name = graphene.String()
    ip_address = graphene.String()

    def resolve_gremlin_host(self, info):
        return get_host(info.context['request'].app.state.graph.connector.gremlin_url)

    def resolve_gremlin_traversal_source(self, info):
        return info.context['request'].app.state.graph.connector.traversal_source

    def resolve_host_name(self, info):
        return get_client_info()['host_name']

    def resolve_ip_address(self, info):
        return get_client_info()['ip_address']


class GenericClientInfoSchema(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="World"))
    get_client_info = graphene.Field(GremlinClientInfo)

    def resolve_hello(self, info, name):
        return name


class ModelVertexSchema(graphene.ObjectType):
    get_vertex_model = graphene.Field(ModelVertexLabel, label=graphene.String())
    get_edge_model = graphene.Field(ModelEdgeLabel, label=graphene.String())
    get_all_vertex_models = graphene.Field(graphene.List(ModelVertexLabel))
    get_all_edges_models = graphene.Field(graphene.List(ModelEdgeLabel))

    def resolve_get_vertex_model(self, info: graphene.ResolveInfo, label: str = None) -> ModelVertexLabel:
        model = info.context['request'].app.state.graph.management.schema_reader.get_vertex_schema(label)
        model.properties = model.properties_as_list()
        return model

    def resolve_get_edge_model(self, info: graphene.ResolveInfo, label: str = None) -> ModelEdgeLabel:
        model = info.context['request'].app.state.graph.management.schema_reader.get_edge_schema(label)
        model.properties = model.properties_as_list()
        return model

    def resolve_get_all_vertex_models(self, info: graphene.ResolveInfo) -> graphene.List(ModelVertexLabel):
        models = info.context['request'].app.state.graph.management.schema_reader.get_all_vertices_schema()
        cleaned_models = []
        for model in models.values():
            model.properties = model.properties_as_list()
            cleaned_models.append(model)
        return cleaned_models

    def resolve_get_all_edges_models(self, info: graphene.ResolveInfo) -> graphene.List(ModelEdgeLabel):
        models = info.context['request'].app.state.graph.management.schema_reader.get_all_edges_schema()
        cleaned_models = []
        for model in models.values():
            model.properties = model.properties_as_list()
            cleaned_models.append(model)
        return cleaned_models
