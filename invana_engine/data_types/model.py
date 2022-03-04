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

from graphene import ObjectType, String, Boolean, List


class ModelProperty(ObjectType):
    name = String()
    cardinality = String()
    type = String()


class LinkPath(ObjectType):
    outv_label = String()
    inv_label = String()


class ModelVertexLabel(ObjectType):
    name = String()
    partitioned = String()
    static = Boolean()
    properties = List(ModelProperty)


class ModelEdgeLabel(ObjectType):
    name = String()
    directed = Boolean()
    unidirected = Boolean()
    multiplicity = String()  # MULTI / MANY2ONE/ ONE2ONE / ONE2MANY
    properties = List(ModelProperty)
    link_paths = List(LinkPath)

    # https://docs.janusgraph.org/schema/#edge-label-multiplicity


class ModelGraphIndex(ObjectType):
    name = String()
    type = String()  # Composite/Mixed
    unique = Boolean()
    backing = String()  # internalindex, search
    key = String()
    status = String()  #


class ModelRelationIndex(ObjectType):
    name = String()
    type = String()
    direction = String()
    sort_key = String()
    order = String()
    status = String()
