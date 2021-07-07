import pytest
from .sample_payloads.sample_data import VERTICES_SAMPLES, EDGES_SAMPLES
from ..settings import TEST_GRAPH_HOST


class TestVerticesOperations:

    @pytest.fixture
    def gremlin_client(self):
        from invana_engine.gremlin.client import GremlinClient
        return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

    @staticmethod
    def drop_all_data(gremlin_client):
        gremlin_client.query("g.V().drop()")

    def create_init_data(self, gremlin_client):
        self.drop_all_data(gremlin_client)

        for vertex_sample in VERTICES_SAMPLES:
            gremlin_client.vertex.create(label=vertex_sample['label'], properties=vertex_sample['properties'])

        for edge_sample in EDGES_SAMPLES:
            from_data = gremlin_client.vertex.read_many(**edge_sample['from_vertex_filters'])
            to_data = gremlin_client.vertex.read_many(**edge_sample['to_vertex_filters'])
            result = gremlin_client.edge.create(
                edge_sample["label"],
                edge_sample["properties"],
                from_data[0]['id'],
                to_data[0]['id']
            )

    def test_vertex_label_schema(self, gremlin_client):
        self.create_init_data(gremlin_client)
        response = gremlin_client.schema.get_vertex_schema("Planet")
        assert response.__len__() == 3
        gremlin_client.close_connection()

    def test_edge_label_schema(self, gremlin_client):
        self.create_init_data(gremlin_client)
        response = gremlin_client.schema.get_edge_schema("has_satellite")
        assert response.__len__() == 1
        gremlin_client.close_connection()

    def test_get_all_edges_schema(self, gremlin_client):
        self.create_init_data(gremlin_client)
        response = gremlin_client.schema.get_all_edges_schema()
        assert isinstance(response, dict)
        assert "has_satellite" in list(response.keys())
        assert response['has_satellite'].__len__() == 1
        gremlin_client.close_connection()

    def test_get_all_vertices_schema(self, gremlin_client):
        self.create_init_data(gremlin_client)
        response = gremlin_client.schema.get_all_vertices_schema()
        assert isinstance(response, dict)
        assert "Planet" in list(response.keys())
        assert response['Planet'].__len__() == 3
        gremlin_client.close_connection()
