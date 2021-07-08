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
from .sample_payloads.client import CLIENT_RAW_QUERIES
from invana_engine.gremlin.client import GremlinClient
from ..settings import TEST_GRAPH_HOST


class TestGremlinClient:

    @pytest.fixture
    def gremlin_client(self):
        return GremlinClient(f"{TEST_GRAPH_HOST}/gremlin")

    def test_create_vertex_query(self, gremlin_client):
        response = gremlin_client.query(CLIENT_RAW_QUERIES['create_query'])
        assert type(response) is list
        gremlin_client.close_connection()

    def test_list_vertex_query(self, gremlin_client):
        response = gremlin_client.query(CLIENT_RAW_QUERIES['list_query'])
        assert type(response) is list
        gremlin_client.close_connection()

    def test_drop_all_query(self, gremlin_client):
        response = gremlin_client.query(CLIENT_RAW_QUERIES['drop_query'])
        count_response = gremlin_client.query(CLIENT_RAW_QUERIES['count_query'])
        assert count_response[0] == 0
        gremlin_client.close_connection()

    def test_vertex_count_query(self, gremlin_client):
        response = gremlin_client.query(CLIENT_RAW_QUERIES['count_query'])
        assert response[0] == 0
        gremlin_client.close_connection()
