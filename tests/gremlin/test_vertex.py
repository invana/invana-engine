import pytest
from .sample_payloads.vertex import CREATE_VERTICES_SAMPLES
from invana_engine.gremlin.core.element import VertexElement
from invana_engine.gremlin.core.exceptions import InvalidQueryArguments
import os

TEST_GRAPH_HOST = os.environ.get("TESTING_HOST")


class TestVertices:

    @pytest.fixture
    def graph_client(self):
        from invana_engine.gremlin import InvanaEngineClient
        return InvanaEngineClient(f"{TEST_GRAPH_HOST}/gremlin")

    def test_create_vertex(self, graph_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            response = graph_client.vertex.create(label=vertex_sample["label"], properties=vertex_sample["properties"])
            assert isinstance(response, VertexElement)

    def test_read_vertex(self, graph_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            props = vertex_sample['properties']
            responses = graph_client.vertex.read_many(
                label=vertex_sample['label'],
                query={list(props.keys())[0]: list(props.values())[0]})
            assert isinstance(responses, list)
            assert isinstance(responses[0], VertexElement)

    def test_update_vertex(self, graph_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            props = vertex_sample['properties']
            response = graph_client.vertex.read_many(label=vertex_sample['label'],
                                                     query={
                                                         list(props.keys())[0]: list(props.values())[0]
                                                     })
            assert isinstance(response, list)
            response2 = graph_client.vertex.update(response[0].id, properties={"new_field": "yeah!"})
            assert isinstance(response2, VertexElement)

    def test_delete_single_vertex(self, graph_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            props = vertex_sample['properties']
            responses = graph_client.vertex.read_many(
                label=vertex_sample['label'],
                query={
                    list(props.keys())[0]: list(props.values())[0]
                }
            )
            assert isinstance(responses, list)
            response2 = graph_client.vertex.delete_one(responses[0].id)

            responses3 = graph_client.vertex.read_one(responses[0].id)
            assert responses3 is None

    def test_delete_vertices(self, graph_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            graph_client.vertex.create(label=vertex_sample['label'],
                                       properties=vertex_sample['properties'])

        graph_client.vertex.delete_many(label=list(CREATE_VERTICES_SAMPLES.keys())[0])
        responses2 = graph_client.vertex.read_many(label=list(CREATE_VERTICES_SAMPLES.keys())[0])
        assert responses2.__len__() == 0

    def test_delete_many_noargs_sent_error(self, graph_client):
        with pytest.raises(InvalidQueryArguments, match=r"label and query"):
            responses = graph_client.vertex.delete_many()

    def test_delete_one_noargs_sent_error(self, graph_client):
        with pytest.raises(TypeError, match=r"missing 1 required positional"):
            responses = graph_client.vertex.delete_one()

    def test_read_one_noargs_sent_error(self, graph_client):
        with pytest.raises(TypeError, match=r"missing 1 required positional"):
            responses = graph_client.vertex.read_one()
