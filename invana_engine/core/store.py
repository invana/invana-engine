from invana_engine.core.utils import convert_to_graphql_schema


class TypeStore:

    def __init__(self):
        # to save the raw schema
        self.node_schema_map = {}
        self.edge_schema_map = {}

        # to save the filters of vertex and edge label
        # ex: battled_where_filters
        self.node_filters_map = {}
        self.edge_filters_map = {}

        # filters based on data type String, Integer, Boolean
        # ex: integer_where_filters
        self.data_type_filters_map = {}


class SchemaStore:
    # store vertex and edge same
    # store in and out edges of vertex
    # store in and out vertices of edges

    def __init__(self, vertices_schema, edges_schema):

        self.vertex_schema_map = {}  # {"battle": {"label": "battle", "properties": []}}
        self.edge_schema_map = {}

        # to save the gql converted schema
        self.vertex_schema_gql_map = {}
        self.edge_schema_gql_map = {}

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
            self.vertex_schema_gql_map[vertex_name] = convert_to_graphql_schema(vertex_schema)

            self.vertex__edges_map[f"{vertex_name}__ine"] = self.get_edges_of_vertex(vertex_name, "inv_label")
            self.vertex__edges_map[f"{vertex_name}__oute"] = self.get_edges_of_vertex(vertex_name, "outv_label")

        for edge_schema in self.edges_schema:
            edge_name = edge_schema['name']
            self.edge_schema_map[edge_name] = edge_schema
            self.edge_schema_gql_map[edge_name] = convert_to_graphql_schema(edge_schema)

            self.edge__vertices_map[f"{edge_name}__inv"] = self.get_vertices_of_edge(edge_name, "inv_label")
            self.edge__vertices_map[f"{edge_name}__outv"] = self.get_vertices_of_edge(edge_name, "outv_label")
