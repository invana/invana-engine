import pytest
from .sample_payloads.client import CLIENT_RAW_QUERIES


class TestGremlinClientClient:

    @pytest.fixture
    def graph_client(self):
        from invana.gremlin import GremlinClient
        return GremlinClient("ws://192.168.0.10:8182/gremlin")

    def test_raw_query(self, graph_client):
        for query_id, raw_query in CLIENT_RAW_QUERIES.items():
            response = graph_client.execute_query(raw_query)
            assert type(response) is list

    def test_drop_everything(self, graph_client):
        response = graph_client.delete_everything()
        # assert response is None
