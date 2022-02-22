#     Copyright 2021 Invana
#  #
#      Licensed under the Apache License, Version 2.0 (the "License");
#      you may not use this file except in compliance with the License.
#      You may obtain a copy of the License at
#  #
#      http:www.apache.org/licenses/LICENSE-2.0
#  #
#      Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.
import os

gremlin_server_url = os.environ.get("GREMLIN_SERVER_URL")
gremlin_server_username = os.environ.get("GREMLIN_SERVER_USERNAME")
gremlin_server_password = os.environ.get("GREMLIN_SERVER_PASSWORD")
gremlin_traversal_source = os.environ.get("GREMLIN_TRAVERSAL_SOURCE", "g")
shall_debug = os.environ.get("DEBUG", False)
server_port = os.environ.get("SERVER_PORT", 8200)
