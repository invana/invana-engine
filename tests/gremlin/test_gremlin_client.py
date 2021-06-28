import pytest
from .sample_payloads.client import CLIENT_RAW_QUERIES
import os
from invana_engine.storages import GremlinClient

TEST_GRAPH_HOST = os.environ.get("TESTING_HOST", "ws://localhost:8182")


class TestGremlinClient:

    @pytest.fixture
    def gremlin_client(self):
        return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

    def test_raw_query(self, gremlin_client):
        for query_id, raw_query in CLIENT_RAW_QUERIES.items():
            response = gremlin_client.execute_query(raw_query)
            assert type(response) is list
        gremlin_client.close()

    # def test_drop_everything(self, gremlin_client):
    #     response = gremlin_client.delete_everything()
    #     # assert response is None
