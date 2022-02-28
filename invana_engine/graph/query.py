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
from invana_engine.utils import get_field_names
from invana_engine.graph.query_resolvers import GremlinGenericQuerySchema
import graphene

from invana_engine.types import NodeType

DEFAULT_LIMIT_SIZE = 10


class TitanPropertiesSchema(graphene.ObjectType):
    # TODO - dynamically generate the fields
    age = graphene.Int()
    name = graphene.String()


class God(NodeType):
    properties = graphene.Field(TitanPropertiesSchema)


class TitanOrderByInputObjectType(graphene.InputObjectType):
    # TODO - dynamically generate the fields
    name = graphene.String()


class WhereFilters(graphene.InputObjectType):
    eq = graphene.String()
    neq = graphene.String()
    startingWith = graphene.String()


class TitanWhereFilters(graphene.InputObjectType):
    name = graphene.Field(WhereFilters)


class TitanSchema(graphene.ObjectType):
    god = graphene.Field(
        graphene.List(God),
        limit=graphene.Argument(graphene.Int, default_value=DEFAULT_LIMIT_SIZE,
                                required=True, description="limits the result count"),
        offset=graphene.Argument(graphene.Int, default_value=0,
                                 description="limits the count"),
        order_by=graphene.Argument(TitanOrderByInputObjectType,
                                   description="order_by"),
        where=graphene.Argument(TitanWhereFilters,
                                description="where")
    )

    def resolve_god(self, info: graphene.ResolveInfo,
                    limit: int = None,
                    offset: int = None,
                    order_by=None,
                    where=None
                    ):
        fields = get_field_names(info)

        search_kwargs = {"has__label": fields['label']}
        if where:
            for property_key, where_item in where.items():
                for predicate_key, predicate_value in where_item.items():
                    search_kwargs[f'has__{property_key}__{predicate_key}'] = predicate_value
        qs = info.context['request'].app.state.graph.vertex.search(**search_kwargs)
        if order_by:
            for order_key, order_value in order_by.items():
                order_value = order_value.lower()
                order_key = f"-{order_key}" if order_value == "desc" else order_key
                qs = qs.order_by(order_key)
        qs = qs.get_traversal()
        if limit and offset:
            qs = qs.range(offset, offset + limit)
        elif limit and not offset:
            qs = qs.limit(limit)
        return [d.to_json() for d in qs.elementMap(*fields['properties']).toList()]


class GraphSchema(GremlinGenericQuerySchema, TitanSchema):
    pass
