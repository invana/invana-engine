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

FIELD_TYPES_MAP = {
    'String': graphene.String,
    'Integer': graphene.Int,
    'class org.janusgraph.core.attribute.Geoshape': graphene.String
    # ...
}

WHERE_CONDITIONS = {
    "eq": graphene.String,
    "neq": graphene.String,

    "lt": graphene.Int,
    "lte": graphene.Int,
    "gt": graphene.Int,
    "gte": graphene.Int,

    "within": lambda: graphene.List(graphene.String),
    "without": lambda: graphene.List(graphene.String),
    "inside": lambda: graphene.List(graphene.String),
    "outside": lambda: graphene.List(graphene.String),
    "between": lambda: graphene.List(graphene.String),

    "startingWith": graphene.String,
    "containing": graphene.String,
    "endingWith": graphene.String,
    "notStartingWith": graphene.String,
    "notContaining": graphene.String,
    "notEndingWith": graphene.String,
}

DEFAULT_LIMIT_SIZE = 10
