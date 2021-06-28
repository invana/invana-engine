import pytest
from .sample_payloads.client import CLIENT_RAW_QUERIES
from invana_engine.gremlin.client import GremlinClient
from ..settings import TEST_GRAPH_HOST


@pytest.fixture
def gremlin_client():
    return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")


class TestGremlinClient:

    def test_raw_query(self, gremlin_client):
        for query_id, raw_query in CLIENT_RAW_QUERIES.items():
            response = gremlin_client.execute_query(raw_query)
            assert type(response) is list
        gremlin_client.close_connection()

    # def test_drop_everything(self, gremlin_client):
    #     response = gremlin_client.delete_everything()
    #     # assert response is None
