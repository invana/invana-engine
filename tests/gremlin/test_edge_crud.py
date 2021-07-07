import pytest
from .sample_payloads.sample_data import VERTICES_SAMPLES, EDGES_SAMPLES
from ..settings import TEST_GRAPH_HOST


class TestEdgesOperations:

    @pytest.fixture
    def gremlin_client(self):
        from invana_engine.gremlin.client import GremlinClient
        return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

    @staticmethod
    def drop_all_data(gremlin_client):
        gremlin_client.query("g.V().drop()")

    @pytest.fixture
    def init_data(self):
        from invana_engine.gremlin.client import GremlinClient
        gremlin_client = GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")
        self.drop_all_data(gremlin_client)
        for vertex_sample in VERTICES_SAMPLES:
            gremlin_client.vertex.get_or_create(label=vertex_sample["label"]
                                                , properties=vertex_sample["properties"])
        _ = gremlin_client.vertex.read_many(has__label__within=["Planet", "Satellite"])
        gremlin_client.close_connection()
        return _

    def test_create_edge(self, gremlin_client, init_data):
        for edge_sample in EDGES_SAMPLES:
            from_data = gremlin_client.vertex.read_many(**edge_sample['from_vertex_filters'])
            to_data = gremlin_client.vertex.read_many(**edge_sample['to_vertex_filters'])
            result = gremlin_client.edge.create(
                edge_sample["label"],
                edge_sample["properties"],
                from_data[0]['id'],
                to_data[0]['id']
            )
            assert isinstance(result, dict)
            assert result['properties']['distance_in_kms'] == edge_sample['properties']['distance_in_kms']
        gremlin_client.close_connection()

    def test_get_or_create_edge(self, gremlin_client, init_data):

        for edge_sample in EDGES_SAMPLES:
            from_data = gremlin_client.vertex.read_many(**edge_sample['from_vertex_filters'])
            to_data = gremlin_client.vertex.read_many(**edge_sample['to_vertex_filters'])
            result = gremlin_client.edge.get_or_create(
                edge_sample["label"],
                edge_sample["properties"],
                from_data[0]['id'],
                to_data[0]['id']
            )
            assert isinstance(result, dict)
            assert result['properties']['distance_in_kms'] == edge_sample['properties']['distance_in_kms']

        gremlin_client.close_connection()

    def test_read_one_noargs_sent_error(self, gremlin_client):
        with pytest.raises(TypeError,
                           match=r"missing 1 required positional argument: 'edge_id'"):
            gremlin_client.edge.read_one()
        gremlin_client.close_connection()

    def test_read_many_edge_with_label(self, gremlin_client):
        edge_labels = list(set([edge_sample['label'] for edge_sample in EDGES_SAMPLES]))
        search_kwargs = {'has__label': edge_labels[0]}
        results = gremlin_client.edge.read_many(**search_kwargs)
        assert isinstance(results, list)
        assert isinstance(results[0], dict)
        for edge in results:
            assert edge['label'] == edge_labels[0]
            assert edge['label'] != edge_labels[1]
        gremlin_client.close_connection()

    def test_update_one_edge(self, gremlin_client):
        edge_labels = list(set([edge_sample['label'] for edge_sample in EDGES_SAMPLES]))
        search_kwargs = {'has__label': edge_labels[0]}
        results = gremlin_client.edge.read_many(**search_kwargs)
        updated_edge = gremlin_client.edge.update_one(results[0]['id'], properties={"new_field": "yeah!"})
        assert isinstance(updated_edge, dict)
        assert updated_edge['properties']['new_field'] == "yeah!"
        updated_edges = gremlin_client.edge.read_many(**search_kwargs)
        for edge in updated_edges:
            if edge['id'] == updated_edge['id']:
                assert edge['properties']['new_field'] == "yeah!"
            else:
                assert edge['properties'].get('new_field') is None
        gremlin_client.close_connection()

    def test_update_many_edges(self, gremlin_client):
        edge_labels = list(set([edge_sample['label'] for edge_sample in EDGES_SAMPLES]))
        result = gremlin_client.edge.update_many(
            has__label=edge_labels[0],
            properties={"new_field": "yeah! updated many working"})
        assert isinstance(result, list)
        for edge in result:
            assert edge['properties']['new_field'] == "yeah! updated many working"
        other_label_result = gremlin_client.edge.read_many(has__label=edge_labels[1])
        for edge in other_label_result:
            assert edge['properties'].get('new_field') is None
        gremlin_client.close_connection()

    def test_delete_single_vertex(self, gremlin_client):
        edge_labels = list(set([edge_sample['label'] for edge_sample in EDGES_SAMPLES]))
        search_kwargs = {'has__label': edge_labels[0]}
        results = gremlin_client.edge.read_many(**search_kwargs)
        edge_id_to_delete = results[0]['id']

        result2 = gremlin_client.edge.delete_one(edge_id_to_delete)
        assert result2 is None
        result3 = gremlin_client.edge.read_one(edge_id_to_delete)
        assert result3 is None
        results = gremlin_client.edge.read_many(**search_kwargs)
        for edge in results:  # data doesnt exist anymore.
            assert edge['id'] != edge_id_to_delete
        gremlin_client.close_connection()

    # def test_delete_many_vertices(self, gremlin_client):
    #     edge_labels = list(set([edge_sample['label'] for edge_sample in EDGES_SAMPLES]))
    #     gremlin_client.edge.delete_many(has__label=edge_labels[0])
    #     results2 = gremlin_client.edge.read_many(has__label=edge_labels[0])
    #     assert results2.__len__() == 0
    #     gremlin_client.close_connection()
