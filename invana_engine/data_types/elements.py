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
import datetime


class AnyField(graphene.Scalar):

    @staticmethod
    def serialize(dt):
        if isinstance(dt, dict):
            transformed_data = {}
            for key, v in dt.items():
                if isinstance(v, datetime.datetime):
                    transformed_data[key] = v.isoformat()
                else:
                    transformed_data[key] = v
            return transformed_data
        elif isinstance(dt, datetime.datetime):
            return dt.isoformat()
        else:
            return dt


class NodeType(graphene.ObjectType):
    id = AnyField()
    type = graphene.String()
    label = graphene.String()
    properties = AnyField()


class InV(graphene.ObjectType):
    id = graphene.ID()
    label = graphene.String()


class OutV(graphene.ObjectType):
    id = graphene.ID()
    label = graphene.String()


class EdgeType(NodeType):
    inv = graphene.Field(InV)
    outv = graphene.Field(OutV)


class NodeOrEdgeType(EdgeType):
    pass
