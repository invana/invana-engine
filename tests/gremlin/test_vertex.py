import pytest
from invana_engine.gremlin.core.types import VertexElement
from invana_engine.gremlin.core.exceptions import InvalidQueryArguments
from .sample_payloads.vertex import CREATE_VERTICES_SAMPLES
from ..settings import TEST_GRAPH_HOST


class TestVerticesOperations:

    @pytest.fixture
    def gremlin_client(self):
        from invana_engine.gremlin.client import GremlinClient
        return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

    def test_create_vertex(self, gremlin_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            result = gremlin_client.vertex.create(
                label=vertex_sample["label"],
                properties=vertex_sample["properties"])
            assert isinstance(result, VertexElement)
        gremlin_client.close_connection()

    def test_read_vertex(self, gremlin_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            props = vertex_sample['properties']
            results = gremlin_client.vertex.read_many(
                label=vertex_sample['label'],
                query={list(props.keys())[0]: list(props.values())[0]})
            assert isinstance(results, list)
            assert isinstance(results[0], VertexElement)
        gremlin_client.close_connection()

    def test_update_vertex(self, gremlin_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            props = vertex_sample['properties']
            result = gremlin_client.vertex.read_many(label=vertex_sample['label'],
                                                       query={
                                                           list(props.keys())[0]: list(props.values())[0]
                                                       })
            assert isinstance(result, list)
            result2 = gremlin_client.vertex.update(result[0].id, properties={"new_field": "yeah!"})
            assert isinstance(result2, VertexElement)
        gremlin_client.close_connection()

    def test_delete_single_vertex(self, gremlin_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            props = vertex_sample['properties']
            results = gremlin_client.vertex.read_many(
                label=vertex_sample['label'],
                query={
                    list(props.keys())[0]: list(props.values())[0]
                }
            )
            assert isinstance(results, list)
            result2 = gremlin_client.vertex.delete_one(results[0].id)

            results3 = gremlin_client.vertex.read_one(results[0].id)
            assert results3 is None
        gremlin_client.close_connection()

    def test_delete_vertices(self, gremlin_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            gremlin_client.vertex.create(label=vertex_sample['label'],
                                         properties=vertex_sample['properties'])

        gremlin_client.vertex.delete_many(label=list(CREATE_VERTICES_SAMPLES.keys())[0])
        results2 = gremlin_client.vertex.read_many(label=list(CREATE_VERTICES_SAMPLES.keys())[0])
        assert results2.__len__() == 0
        gremlin_client.close_connection()

    def test_delete_many_noargs_sent_error(self, gremlin_client):
        with pytest.raises(InvalidQueryArguments,
                           match="Both label and query arguments cannot be none"
                           ):
            results = gremlin_client.vertex.delete_many()
        gremlin_client.close_connection()

    def test_delete_one_noargs_sent_error(self, gremlin_client):
        with pytest.raises(TypeError, match=r"missing 1 required positional"):
            results = gremlin_client.vertex.delete_one()
        gremlin_client.close_connection()

    def test_read_one_noargs_sent_error(self, gremlin_client):
        with pytest.raises(TypeError, match=r"missing 1 required positional"):
            results = gremlin_client.vertex.read_one()
        gremlin_client.close_connection()
