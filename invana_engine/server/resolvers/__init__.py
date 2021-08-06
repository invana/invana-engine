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
from ariadne import MutationType, SubscriptionType, QueryType
from .vertex import VertexOps
from .generic import GenericOps

# vertex_ops = VertexOps()
generic_ops = GenericOps()

# mutation_type = MutationType()
# subscription_type = SubscriptionType()
query_type = QueryType()

query_type.set_field("executeQuery", generic_ops.resolve_execute_query)

# mutation_type.set_field("createVertex", vertex_ops.resolve_create_vertex)
