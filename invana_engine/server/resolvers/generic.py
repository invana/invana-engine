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
import logging

logger = logging.getLogger(__name__)


class GenericOps:

    @staticmethod
    async def resolve_execute_query(_, info, gremlinQuery=None):
        """

        :param _:
        :param info:
        :param gremlinQuery:

        :return:
        """
        logger.info("Executing query: {gremlinQuery}".format(gremlinQuery=gremlinQuery))
        result = await  info.context['gremlin_client'].execute_query(gremlinQuery)
        return [element.to_value() for element in result]
