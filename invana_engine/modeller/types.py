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
import graphene


class ModelProperty(graphene.ObjectType):
    name = graphene.String()
    cardinality = graphene.String()
    type = graphene.String()


class LinkPath(graphene.ObjectType):
    outv_label = graphene.String()
    inv_label = graphene.String()


class ModelVertexLabel(graphene.ObjectType):
    name = graphene.String()
    partitioned = graphene.String()
    static = graphene.Boolean()
    properties = graphene.List(ModelProperty)


class ModelEdgeLabel(graphene.ObjectType):
    name = graphene.String()
    directed = graphene.Boolean()
    unidirected = graphene.Boolean()
    multiplicity = graphene.String()  # MULTI / MANY2ONE/ ONE2ONE / ONE2MANY
    properties = graphene.List(ModelProperty)
    link_paths = graphene.List(LinkPath)

    # https://docs.janusgraph.org/schema/#edge-label-multiplicity


class ModelGraphIndex(graphene.ObjectType):
    name = graphene.String()
    type = graphene.String()  # Composite/Mixed
    unique = graphene.Boolean()
    backing = graphene.String()  # internalindex, search
    key = graphene.String()
    status = graphene.String()  #


class ModelRelationIndex(graphene.ObjectType):
    name = graphene.String()
    type = graphene.String()
    direction = graphene.String()
    sort_key = graphene.String()
    order = graphene.String()
    status = graphene.String()
