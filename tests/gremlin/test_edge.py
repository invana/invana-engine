import pytest
from .sample_payloads.vertex import CREATE_VERTICES_SAMPLES
from .sample_payloads.edge import CREATE_EDGES_SAMPLES
from invana_engine.gremlin.core.element import EdgeElement
from invana_engine.gremlin.core.exceptions import InvalidQueryArguments
import os

TEST_GRAPH_HOST = os.environ.get("TESTING_HOST")


class TestEdges:

    @pytest.fixture
    def graph_client(self):
        from invana_engine.gremlin import InvanaEngineClient
        return InvanaEngineClient(f"{TEST_GRAPH_HOST}/gremlin")

    @pytest.fixture
    def init_data(self):
        from invana_engine.gremlin import InvanaEngineClient
        graph_client = InvanaEngineClient(f"{TEST_GRAPH_HOST}/gremlin")
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            graph_client.vertex.create(label=vertex_sample["label"], properties=vertex_sample["properties"])
        return graph_client.vertex.read_many()

    def test_create_edge(self, graph_client, init_data):
        for k, edge_sample in CREATE_EDGES_SAMPLES.items():
            graph_client.edge.create(
                label=edge_sample["label"],
                properties=edge_sample["properties"],
                inv=init_data[0].id,
                outv=init_data[1].id
            )

    def test_read_edge(self, graph_client):
        for k, edge_sample in CREATE_EDGES_SAMPLES.items():
            props = edge_sample['properties']
            responses = graph_client.edge.read_many(
                label=edge_sample['label'],
                query={list(props.keys())[0]: list(props.values())[0]})
            assert isinstance(responses, list)
            assert isinstance(responses[0], EdgeElement)

    def test_update_edge(self, graph_client):
        for k, edge_sample in CREATE_EDGES_SAMPLES.items():
            props = edge_sample['properties']
            response = graph_client.edge.read_many(
                label=edge_sample['label'],
                query={list(props.keys())[0]: list(props.values())[0]}
            )
            assert isinstance(response, list)
            response2 = graph_client.edge.update(response[0].id, properties={"new_field": "yeah!"})
            assert isinstance(response2, EdgeElement)

    def test_delete_single_edge(self, graph_client):
        for k, edge_sample in CREATE_EDGES_SAMPLES.items():
            props = edge_sample['properties']
            responses = graph_client.edge.read_many(
                label=edge_sample['label'],
                query={
                    list(props.keys())[0]: list(props.values())[0]
                }
            )
            assert isinstance(responses, list)
            response2 = graph_client.edge.delete_one(responses[0].id)
            responses3 = graph_client.edge.read_one(responses[0].id)
            assert responses3 is None

    def test_delete_edges(self, graph_client, init_data):
        for k, edge_sample in CREATE_EDGES_SAMPLES.items():
            graph_client.edge.create(
                label=edge_sample["label"],
                properties=edge_sample["properties"],
                inv=init_data[0].id,
                outv=init_data[1].id
            )
        responses = graph_client.edge.delete_many(label="has_satellite")
        responses2 = graph_client.edge.read_many(label="has_satellite")
        assert responses2.__len__() == 0

    def test_delete_many_noargs_sent_error(self, graph_client):
        with pytest.raises(InvalidQueryArguments, match=r"label and query"):
            responses = graph_client.edge.delete_many()

    def test_delete_one_noargs_sent_error(self, graph_client):
        with pytest.raises(TypeError, match=r"missing 1 required positional"):
            responses = graph_client.edge.delete_one()

    def test_read_one_noargs_sent_error(self, graph_client):
        with pytest.raises(TypeError, match=r"missing 1 required positional"):
            responses = graph_client.edge.read_one()
