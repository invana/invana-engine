#  Copyright 2021 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from invana_engine2.graph.query_resolvers import GremlinGenericQuerySchema
import graphene
from invana_engine2.settings import __VERSION__


class GraphSchema(GremlinGenericQuerySchema):
    _version = graphene.String()

    def resolve__version(self, info: graphene.ResolveInfo) -> str:
        return __VERSION__
