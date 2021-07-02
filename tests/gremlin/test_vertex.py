import pytest
from invana_engine.gremlin.core.exceptions import InvalidQueryArguments
from .sample_payloads.vertex import CREATE_VERTICES_SAMPLES
from ..settings import TEST_GRAPH_HOST


class TestVerticesOperations:

    @pytest.fixture
    def gremlin_client(self):
        from invana_engine.gremlin.client import GremlinClient
        return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

    @staticmethod
    def create_init_data(gremlin_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            gremlin_client.vertex.create(label=vertex_sample['label'], properties=vertex_sample['properties'])
        gremlin_client.close_connection()

    @staticmethod
    def delete_all_data(gremlin_client):
        pass
        # gremlin_client.search("g.V().drop()")
        # gremlin_client.close_connection()

    def test_create_vertex(self, gremlin_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            result = gremlin_client.vertex.create(
                label=vertex_sample["label"],
                properties=vertex_sample["properties"])
            assert isinstance(result, dict)
        gremlin_client.close_connection()

    def test_read_one_noargs_sent_error(self, gremlin_client):
        with pytest.raises(TypeError,
                           match=r"missing 1 required positional argument: 'vertex_id'"):
            results = gremlin_client.vertex.read_one()
        gremlin_client.close_connection()

    def test_read_many_vertex(self, gremlin_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            _ = gremlin_client.vertex.create(label=vertex_sample['label'], properties=vertex_sample['properties'])

        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            search_kwargs = {
                'has__label': vertex_sample['label'],
                # 'has__label': "Planet",
                # "has__{}".format(list(props.keys())[0]): list(props.values())[0]
            }
            results = gremlin_client.vertex.read_many(**search_kwargs)
            assert isinstance(results, list)
            assert isinstance(results[0], dict)
        gremlin_client.close_connection()

    def test_update_one_vertex(self, gremlin_client):
        # self.create_init_data(gremlin_client)
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            props = vertex_sample['properties']
            result = gremlin_client.vertex.read_many(has__label=vertex_sample['label'])
            assert isinstance(result, list)
            result2 = gremlin_client.vertex.update_one(result[0]['id'], properties={"new_field": "yeah!"})
            assert isinstance(result2, dict)
        gremlin_client.close_connection()

    def test_update_many_vertices(self, gremlin_client):
        # self.create_init_data(gremlin_client)
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            result2 = gremlin_client.vertex.update_many(
                has__label=vertex_sample['label'],
                properties={"new_field": "yeah! updated many working"})
            assert isinstance(result2, list)
        # self.delete_all_data(gremlin_client)
        gremlin_client.close_connection()

    # def test_delete_single_vertex(self, gremlin_client):
    #     self.create_init_data(gremlin_client)
    #     for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
    #         results = gremlin_client.vertex.read_many(has__label=vertex_sample['label'], )
    #         assert isinstance(results, list)
    #         result2 = gremlin_client.vertex.delete_one(results[0].id)
    #         results3 = gremlin_client.vertex.read_one(results[0].id)
    #         assert results3 is None
    #     self.delete_all_data(gremlin_client)
    #     gremlin_client.close_connection()

    # def test_delete_vertices(self, gremlin_client):
    #     self.create_init_data(gremlin_client)
    #     # for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
    #     #     gremlin_client.vertex.create(label=vertex_sample['label'], properties=vertex_sample['properties'])
    #
    #     gremlin_client.vertex.delete_many(has__label=list(CREATE_VERTICES_SAMPLES.keys())[0])
    #     results2 = gremlin_client.vertex.read_many(has__label=list(CREATE_VERTICES_SAMPLES.keys())[0])
    #     assert results2.__len__() == 0
    #     self.delete_all_data(gremlin_client)
    #     gremlin_client.close_connection()
    #
    def test_delete_many_noargs_sent_error(self, gremlin_client):
        with pytest.raises(
                InvalidQueryArguments,
                # match=r"Either has__** or pagination__** search kwargs"
        ):
            results = gremlin_client.vertex.delete_many()
        gremlin_client.close_connection()

    def test_delete_one_noargs_sent_error(self, gremlin_client):
        with pytest.raises(TypeError,
                           match=r"missing 1 required positional argument: 'vertex_id'"):
            results = gremlin_client.vertex.delete_one()
        gremlin_client.close_connection()

    #
