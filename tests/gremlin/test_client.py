import pytest
from .sample_payloads.client import CLIENT_RAW_QUERIES
import os

TEST_GRAPH_HOST = os.environ.get("TESTING_HOST")


class TestGremlinClientClient:

    @pytest.fixture
    def graph_client(self):
        from invana_engine.gremlin import InvanaEngineClient
        return InvanaEngineClient(f"{TEST_GRAPH_HOST}/gremlin")

    def test_raw_query(self, graph_client):
        for query_id, raw_query in CLIENT_RAW_QUERIES.items():
            response = graph_client.execute_query(raw_query)
            assert type(response) is list

    def test_drop_everything(self, graph_client):
        response = graph_client.delete_everything()
        # assert response is None
