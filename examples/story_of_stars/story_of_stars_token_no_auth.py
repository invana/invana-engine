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
from invana_engine.gremlin.client import GremlinClient
import os
import json


class StoryOfStarsGraph:

    def __init__(self, gremlin_server_url, auth=None):
        self.gremlin_client = GremlinClient(gremlin_server_url, auth=auth)

    def create_vertices(self, vertices):
        for vertex_sample in vertices:
            self.gremlin_client.vertex.get_or_create(
                label=vertex_sample["label"],
                properties=vertex_sample["properties"])

    def create_edges(self, edges):
        for edge in edges:
            from_data = self.gremlin_client.vertex.read_many(**edge['from_vertex_filters'])
            to_data = self.gremlin_client.vertex.read_many(**edge['to_vertex_filters'])
            self.gremlin_client.edge.get_or_create(
                edge["label"],
                edge["properties"],
                from_data[0]['id'],
                to_data[0]['id']
            )

    def close(self):
        self.gremlin_client.close_connection()


if __name__ == "__main__":
    gremlin_url = os.environ.get("GREMLIN_SERVER_URL", "ws://192.168.0.10:8182/gremlin")
    star_graph = StoryOfStarsGraph(gremlin_url)
    data = json.load(open("data.json"))
    star_graph.create_vertices(data['VERTICES_SAMPLES'])
    star_graph.create_edges(data['EDGES_SAMPLES'])
    print("importing graph done")
