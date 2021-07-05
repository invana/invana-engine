import pytest
from .sample_payloads.schema import SCHEMA_SAMPLE_DATA
from ..settings import TEST_GRAPH_HOST


class TestVerticesOperations:

    @pytest.fixture
    def gremlin_client(self):
        from invana_engine.gremlin.client import GremlinClient
        return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

    @staticmethod
    def create_init_data(gremlin_client):
        for vertex_sample in SCHEMA_SAMPLE_DATA:
            gremlin_client.vertex.create(label=vertex_sample['label'], properties=vertex_sample['properties'])
        # gremlin_client.close_connection()

    def test_vertex_label_schema(self, gremlin_client):
        self.create_init_data(gremlin_client)
        response = gremlin_client.schema.get_vertex_schema("Teacher")
        assert response['propertyKeys'].__len__() == 3
        gremlin_client.close_connection()
