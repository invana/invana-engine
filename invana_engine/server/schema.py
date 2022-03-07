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
import graphene
from invana_engine.core.schema_generator import DynamicSchemaGenerator
from invana_engine.core.utils import convert_to_graphql_schema
from .graph import graph
from invana_engine.modeller.query import ModellerQuery
from invana_engine.graph.query import GraphSchema


class SchemaStore:
    # store vertex and edge same
    # store in and out edges of vertex
    # store in and out vertices of edges

    def __init__(self, vertices_schema, edges_schema):

        self.vertex_schema_map = {}  # {"battle": {"label": "battle", "properties": []}}
        self.edge_schema_map = {}
        self.vertex__edges_map = {}  # battle__ine : ['god']
        self.edge__vertices_map = {}

        self.vertices_schema = vertices_schema
        self.edges_schema = edges_schema
        self.generate_map()

    def get_edges_of_vertex(self, vertex_label, label_type: ["inv_label", "outv_label"]):
        edges = []
        for edge_schema in self.edges_schema:
            for link_path in edge_schema['link_paths']:
                if link_path[label_type] == vertex_label:
                    edges.append(edge_schema['name'])
        return list(set(edges))

    def get_vertices_of_edge(self, edge_label, label_type):
        vertices = []
        edge_schema = self.edge_schema_map[edge_label]
        for link_path in edge_schema['link_paths']:
            vertices.append(link_path[label_type])
        return list(set(vertices))

    def generate_map(self):
        for vertex_schema in self.vertices_schema:
            vertex_name = vertex_schema['name']
            self.vertex_schema_map[vertex_name] = vertex_schema

            self.vertex__edges_map[f"{vertex_name}__ine"] = self.get_edges_of_vertex(vertex_name, "inv_label")
            self.vertex__edges_map[f"{vertex_name}__oute"] = self.get_edges_of_vertex(vertex_name, "outv_label")

        for edge_schema in self.edges_schema:
            edge_name = edge_schema['name']
            self.edge_schema_map[edge_name] = edge_schema

            self.edge__vertices_map[f"{edge_name}__inv"] = self.get_vertices_of_edge(edge_name, "inv_label")
            self.edge__vertices_map[f"{edge_name}__outv"] = self.get_vertices_of_edge(edge_name, "outv_label")


def get_schema():
    vertices_schema_objects = graph.management.schema_reader.get_all_vertices_schema()
    vertices_schema_json = [schema.to_json() for key, schema in vertices_schema_objects.items()]

    vertices_schema_data_json = convert_to_graphql_schema(vertices_schema_json)

    edges_schema_objects = graph.management.schema_reader.get_all_edges_schema()
    edges_schema_json = [schema.to_json() for key, schema in edges_schema_objects.items()]
    edges_schema_data_json = convert_to_graphql_schema(edges_schema_json)


    schema_store = SchemaStore(vertices_schema_json, edges_schema_json)

    vertices_schema_generator = DynamicSchemaGenerator(vertices_schema_data_json, "node", schema_store)
    edge_schema_generator = DynamicSchemaGenerator(edges_schema_data_json, "edge", schema_store)


    all_properties = {}
    for vertices_schema in vertices_schema_json:
        for prop in vertices_schema['properties']:
            all_properties[prop['name']] = prop
    for edges_schema in edges_schema_json:
        for prop in edges_schema['properties']:
            all_properties[prop['name']] = prop

    # vertex_search_schema_data_json = [{
    #     "id": "search_vertices",
    #     "name": "search_vertices",
    #     "properties": all_properties.values(),
    # }]
    # vertex_search_schema_data_json = convert_to_graphql_schema(vertex_search_schema_data_json)
    # vertex_search_schema_generator = DynamicSchemaGenerator(vertex_search_schema_data_json, "node",
    #                                                         is_global_search=True)
    #
    # edge_search_schema_data_json = [{
    #     "id": "search_edge",
    #     "name": "search_edge",
    #     "properties": all_properties.values(),
    # }]
    # edge_search_schema_data_json = convert_to_graphql_schema(edge_search_schema_data_json)
    # edge_search_schema_generator = DynamicSchemaGenerator(edge_search_schema_data_json, "edge", is_global_search=True)

    NodeQuery, node_record_schema_types = vertices_schema_generator.create_schema_dynamically()
    EdgeQuery, edge_record_schema_types = edge_schema_generator.create_schema_dynamically()

    # SearchVertexSearchQuery, vertex_search_record_schema_types = vertex_search_schema_generator.create_schema_dynamically()
    # SearchEdgeSearchQuery, edge_search_record_schema_types = edge_search_schema_generator.create_schema_dynamically()

    # class Query(ModellerQuery, GraphSchema, NodeQuery, EdgeQuery, SearchVertexSearchQuery, SearchEdgeSearchQuery):
    class Query(ModellerQuery, GraphSchema, NodeQuery, EdgeQuery):
        pass

    return graphene.Schema(query=Query,
                           types=node_record_schema_types + edge_record_schema_types,
                           # + vertex_search_record_schema_types + edge_search_record_schema_types,
                           auto_camelcase=False
                           )
