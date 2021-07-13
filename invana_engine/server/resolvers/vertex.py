#  Copyright 2020 Invana
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http:www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import json
import logging

logger = logging.getLogger(__name__)


class VertexOps:

    @staticmethod
    async def resolve_create_vertex(_, info, label=None, properties=None):
        """

        :param _:
        :param info:
        :param label:
        :param properties:
        :return:
        """
        logger.info("Creating vertex with label {label} and properties {properties}".format(
            label=label, properties=properties))
        properties = json.loads(properties)
        gremlin_client = info.context['gremlin_client']
        _ = gremlin_client.vertex.create(label=label, properties=properties)
        print("====", _)
        return True
