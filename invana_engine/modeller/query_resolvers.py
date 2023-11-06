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
from ..utils import get_host, get_client_info, snake_case_to_camel_case
from invana_engine.data_types import LabelSchemaEdgeType, LabelSchemaVertexType, AnyField
import graphene
import json


class FeaturesInfo(graphene.ObjectType):
    graph_features = AnyField()
    variable_features = AnyField()
    vertex_features = AnyField()
    edge_features = AnyField()
    vertex_property_features = AnyField()
    edge_property_features = AnyField()


class GremlinClientInfo(graphene.ObjectType):
    gremlin_host = graphene.String()
    gremlin_traversal_source = graphene.String()
    host_name = graphene.String()
    host_ip_address = graphene.String()
    features = graphene.Field(FeaturesInfo)

    def resolve_features(self, info):
        features_data = info.context['request'].app.state.graph.connector.get_features().data
        data = {}
        for k, v in features_data.items():
            data[snake_case_to_camel_case(k)] = v
        return data


class GenericClientInfoSchema(graphene.ObjectType):
    _hello = graphene.String(name=graphene.String(default_value="World"))
    _get_client_info = graphene.Field(GremlinClientInfo)

    def resolve__hello(self, info, name):
        return name

    def resolve__get_client_info(self, info):
        result = get_client_info()
        result['gremlin_host'] = get_host(info.context['request'].app.state.graph.connector.connection_uri)
        result['gremlin_traversal_source'] = info.context['request'].app.state.graph.connector.traversal_source
        return result


class LabelSchemaObjectTypes(graphene.ObjectType):
    schema_get_vertex_schema = graphene.Field(LabelSchemaVertexType, label=graphene.String())
    schema_get_edge_schema = graphene.Field(LabelSchemaEdgeType, label=graphene.String())

    schema_get_vertex_label_property_keys = graphene.List(graphene.String, label=graphene.String())
    schema_get_edge_label_property_keys = graphene.List(graphene.String, label=graphene.String())

    schema_get_all_vertex_schema = graphene.Field(graphene.List(LabelSchemaVertexType))
    schema_get_all_edge_schema = graphene.Field(graphene.List(LabelSchemaEdgeType))

    schema_get_vertex_labels = graphene.Field(graphene.List(graphene.String))
    schema_get_edge_labels = graphene.Field(graphene.List(graphene.String))

    # get_vertex_label_schema = graphene.Field(VertexSchemaType, label=graphene.String())
    # get_edge_label_schema = graphene.Field(EdgeSchemaType, label=graphene.String())

    def resolve_schema_get_vertex_label_property_keys(self, info: graphene.ResolveInfo, label: str = None) -> any:
        return info.context['request'].app.state.graph.management.schema_reader.get_vertex_property_keys(label)

    def resolve_schema_get_edge_label_property_keys(self, info: graphene.ResolveInfo, label: str = None) -> any:
        return info.context['request'].app.state.graph.management.schema_reader.get_edge_property_keys(label)

    def resolve_schema_get_vertex_labels(self, info: graphene.ResolveInfo) -> any:
        return info.context['request'].app.state.graph.management.schema_reader.get_all_vertex_labels()

    def resolve_schema_get_edge_labels(self, info: graphene.ResolveInfo) -> any:
        return info.context['request'].app.state.graph.management.schema_reader.get_all_edge_labels()

    #
    # def resolve_get_vertex_label_schema(self, info: graphene.ResolveInfo, label: str = None) -> any:
    #     return info.context['request'].app.state.graph.schema_reader.get_vertex_schema(label)
    #
    # def resolve_get_edge_label_schema(self, info: graphene.ResolveInfo, label: str = None) -> any:
    #     return info.context['request'].app.state.graph.schema_readr.get_edge_schema(label)

    def resolve_schema_get_vertex_schema(self, info: graphene.ResolveInfo, label: str = None) -> LabelSchemaVertexType:
        model = info.context['request'].app.state.graph.management.schema_reader.get_vertex_schema(label)
        return model.to_json()

    def resolve_schema_get_edge_schema(self, info: graphene.ResolveInfo, label: str = None) -> LabelSchemaEdgeType:
        model = info.context['request'].app.state.graph.management.schema_reader.get_edge_schema(label)
        return model.to_json()

    def resolve_schema_get_all_vertex_schema(self, info: graphene.ResolveInfo) -> graphene.List(LabelSchemaVertexType):
        models = info.context['request'].app.state.graph.management.schema_reader.get_all_vertices_schema()
        cleaned_models = []
        for model in models.values():
            cleaned_models.append(model.to_json())
        return cleaned_models

    def resolve_schema_get_all_edge_schema(self, info: graphene.ResolveInfo) -> graphene.List(LabelSchemaEdgeType):
        models = info.context['request'].app.state.graph.management.schema_reader.get_all_edges_schema()
        cleaned_models = []
        for model in models.values():
            cleaned_models.append(model.to_json())
        return cleaned_models
