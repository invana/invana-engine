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
# implementation inspired from - https://stackoverflow.com/a/52690104
import graphene
from invana_engine.graph.query import GraphSchema
from invana_engine.utils import get_field_names
from invana_engine.types import NodeType
from invana_engine.modeller.query import ModellerQuery
from .utils import convert_to_graphql_schema
from .constants import FIELD_TYPES_MAP, WHERE_CONDITIONS, DEFAULT_LIMIT_SIZE

class_definition_example = [
    {
        "name": "titan",
        "properties": [
            {

                "name": "age",
                "cardinality": "SINGLE",
                "type": "Integer"
            },
            {
                "name": "name",
                "cardinality": "SINGLE",
                "type": "String"
            }
        ]
    }
]


class DynamicSchemaGenerator:

    def __init__(self, schema_data):
        self.schema_data = schema_data

    def create_resolver(self, record_name, record_cls):
        def resolver_func(self, info: graphene.ResolveInfo,
                          limit: int = None,
                          offset: int = None,
                          order_by=None,
                          where=None
                          ):
            fields = get_field_names(info)
            search_kwargs = {"has__label": fields['label']}
            if where:
                for property_key, where_item in where.items():
                    if where_item:
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
            data = [record_cls(**d.to_json()) for d in qs.elementMap(*fields['properties']).toList()]
            return data

        resolver_func.__name__ = 'resolve_%s' % record_name
        return resolver_func

    def create_record_type(self, classname, properties, element_type):
        record_properties_type = type(
            f"{classname}Properties",
            (graphene.ObjectType,),
            properties
        )
        record_extra_fields = {"properties": graphene.Field(record_properties_type)}
        record_type = type(
            f"{classname}{element_type.capitalize()}Type",
            (NodeType,),
            record_extra_fields
        )
        return record_type

    def create_record_fields(self, record_class, property_keys):
        order_by_fields = {}
        for property_key in property_keys:
            order_by_fields[property_key] = graphene.String()
        order_by_type = type(
            f"{record_class.__name__}OrderBy",
            (graphene.InputObjectType,),
            order_by_fields
        )

        where_filter_fields = {}
        for where_condition_key, where_condition_type in WHERE_CONDITIONS.items():
            where_filter_fields[where_condition_key] = where_condition_type()

        where_filters = type(
            f"WhereFilters",
            (graphene.InputObjectType,),
            where_filter_fields
        )

        node_type_where_filters = {}
        for property_key in property_keys:
            node_type_where_filters[property_key] = graphene.Field(where_filters)
        where_filters = type(
            f"{record_class.__name__}WhereFilters",
            (graphene.InputObjectType,),
            node_type_where_filters
        )
        return graphene.Field(
            graphene.List(record_class),
            limit=graphene.Argument(graphene.Int, default_value=DEFAULT_LIMIT_SIZE,
                                    required=True, description="limits the result count"),
            offset=graphene.Argument(graphene.Int, default_value=0,
                                     description="limits the count"),
            order_by=graphene.Argument(order_by_type,
                                       description="order_by"),
            where=graphene.Argument(where_filters,
                                    description="where")
        )

    def create_schema_dynamically(self):
        record_schemas = {}
        record_properties = {}
        for record_type in self.schema_data:
            classname = record_type["id"]  # 'Author'
            properties = {}
            record_properties[record_type['id']] = []
            for option in record_type["options"]:
                field_type = FIELD_TYPES_MAP[option['type']]
                properties[option['id']] = field_type()  # maybe add label as description
                record_properties[record_type['id']].append(option['id'])
            record_schemas[record_type['id']] = self.create_record_type(
                classname,
                properties,
                "node"
            )
        # create Query in similar way
        record_fields = {}
        for key, rec in record_schemas.items():
            record_fields[key] = self.create_record_fields(rec, record_properties[key])  # graphene.Field(rec)
            record_fields['resolve_%s' % key] = self.create_resolver(key, rec)
        NodeQuery = type('NodeQuery', (graphene.ObjectType,), record_fields)

        class Query(ModellerQuery, GraphSchema, NodeQuery):
            pass

        return graphene.Schema(query=Query, types=list(record_schemas.values()))


schema_data_json = convert_to_graphql_schema(class_definition_example)
schema_generator = DynamicSchemaGenerator(schema_data_json)
schema = schema_generator.create_schema_dynamically()

# class Query(ModellerQuery, GraphSchema):
#     pass
#
#
# schema = graphene.Schema(query=Query)  # , mutation=Mutation, subscription=Subscription)
