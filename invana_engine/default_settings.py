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
import os

GREMLIN_SERVER_SETTINGS = {
    "gremlin_server_url": os.environ.get("GREMLIN_SERVER_URL", "ws://192.168.0.10:8182/gremlin"),
    "traversal_source": os.environ.get("GREMLIN_TRAVERSAL_SOURCE", "g"),
    "serializer_class": "invana_engine.gremlin.serializers.graphson_v3.GraphSONV3Reader",
    "gremlin_server_username": os.environ.get("GRAPHQL_USERNAME"),
    "gremlin_server_password": os.environ.get("GRAPHQL_PASSWORD"),
    "ALLOW_FILTERING": int(os.environ.get("ALLOW_FILTERING", "0")),
    "IGNORE_UNINDEXED": int(os.environ.get("IGNORE_UNINDEXED", "0"))

}

GRAPHQL_SERVER_SETTINGS = {
    "server_port": int(os.environ.get("SERVER_PORT", 8200))
}

__DEBUG__ = os.environ.get("DEBUG", True)

__VERSION__ = "0.0.12"
