import pytest
from .sample_payloads.vertex import CREATE_VERTICES_SAMPLES
from .sample_payloads.edge import CREATE_EDGES_SAMPLES
from invana_engine.gremlin.core.types import EdgeElement
from invana_engine.gremlin.core.exceptions import InvalidQueryArguments
from ..settings import TEST_GRAPH_HOST


class TestEdgesOperations:

    @pytest.fixture
    def gremlin_client(self):
        from invana_engine.gremlin.client import GremlinClient
        return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

    @pytest.fixture
    def init_data(self):
        from invana_engine.gremlin.client import GremlinClient
        gremlin_client = GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            gremlin_client.vertex.get_or_create(label=vertex_sample["label"], properties=vertex_sample["properties"])

        _ = gremlin_client.vertex.read_many(has__label__within=["Planet", "Satellite"])
        gremlin_client.close_connection()
        return _

    # def test_create_edge(self, gremlin_client, init_data):
    #     for k, edge_sample in CREATE_EDGES_SAMPLES.items():
    #         result = gremlin_client.edge.create(
    #             edge_sample["label"],
    #             edge_sample["properties"],
    #             init_data[0]['id'],
    #             init_data[1]['id']
    #         )
    #         assert isinstance(result, dict)
    #     gremlin_client.close_connection()

    def test_get_or_create_edge(self, gremlin_client, init_data):
        for k, edge_sample in CREATE_EDGES_SAMPLES.items():
            result = gremlin_client.edge.get_or_create(
                edge_sample["label"],
                edge_sample["properties"],
                # {},
                init_data[0]['id'],
                init_data[1]['id']
            )
            assert isinstance(result, dict)


        gremlin_client.close_connection()
