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

gremlin_client = GremlinClient("ws://192.168.0.10:8182/gremlin")

gremlin_client.indexes.composite_index.create_vertex_index(
    "byNameRadiusPlanet", "Planet", ["name", "radius_in_kms"]
)
