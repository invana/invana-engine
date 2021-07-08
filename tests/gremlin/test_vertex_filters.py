#  Copyright 2020 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import pytest
from .sample_payloads.vertex import CREATE_VERTICES_SAMPLES
from ..settings import TEST_GRAPH_HOST


class TestVertexFiltersOperations:

    @pytest.fixture
    def gremlin_client(self):
        from invana_engine.gremlin.client import GremlinClient
        return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

    @staticmethod
    def create_init_data(gremlin_client):
        for k, vertex_sample in CREATE_VERTICES_SAMPLES.items():
            gremlin_client.vertex.create(label=vertex_sample['label'], properties=vertex_sample['properties'])
        # gremlin_client.close_connection()

    @staticmethod
    def delete_all_data(gremlin_client):
        gremlin_client.query("g.V().drop()")
        # gremlin_client.close_connection()

    def test_read_many_vertex_using_has__within(self, gremlin_client):
        self.delete_all_data(gremlin_client)
        self.create_init_data(gremlin_client)
        labels = [v['label'] for k, v in CREATE_VERTICES_SAMPLES.items()]
        search_kwargs = {'has__label__within': [labels[0]]}
        results = gremlin_client.vertex.read_many(**search_kwargs)
        assert isinstance(results, list)
        assert isinstance(results[0], dict)
        assert results[0]['label'], labels[0]
        assert results.__len__() == 1
        gremlin_client.close_connection()

    def test_read_many_vertex_using_has__without(self, gremlin_client):
        labels = [v['label'] for k, v in CREATE_VERTICES_SAMPLES.items()]
        search_kwargs = {'has__label__without': [labels[0]]}
        results = gremlin_client.vertex.read_many(**search_kwargs)
        assert isinstance(results, list)
        assert isinstance(results[0], dict)
        assert results[0]['label'] == labels[1]
        gremlin_client.close_connection()

    def test_read_many_vertex_using_has__id(self, gremlin_client):
        results = gremlin_client.vertex.read_many(has__label="Planet")
        search_kwargs = {'has__id': results[0]['id']}
        new_results = gremlin_client.vertex.read_many(**search_kwargs)
        assert results[0]['id'] == new_results[0]['id']
        gremlin_client.close_connection()

    def test_read_many_vertex_using_has__label(self, gremlin_client):
        labels = [v['label'] for k, v in CREATE_VERTICES_SAMPLES.items()]
        search_kwargs = {'has__label': labels[0]}
        results = gremlin_client.vertex.read_many(**search_kwargs)
        assert results[0]['label'] == labels[0]
        gremlin_client.close_connection()

    def test_read_many_vertex_using_has__name(self, gremlin_client):
        name_properties = [v['properties']['name'] for k, v in CREATE_VERTICES_SAMPLES.items()]
        search_kwargs = {'has__name': name_properties[0]}
        results = gremlin_client.vertex.read_many(**search_kwargs)
        assert results[0]['properties']['name'] == name_properties[0]
        gremlin_client.close_connection()

    def test_read_many_vertex_using_pagination__limit(self, gremlin_client):
        search_kwargs = {'pagination__limit': 1}
        results = gremlin_client.vertex.read_many(**search_kwargs)
        assert results.__len__() == 1
        gremlin_client.close_connection()

    def test_read_many_vertex_using_pagination__range(self, gremlin_client):
        search_kwargs = {'pagination__range': (0, 1)}
        results = gremlin_client.vertex.read_many(**search_kwargs)
        assert results.__len__() == 1
        gremlin_client.close_connection()
