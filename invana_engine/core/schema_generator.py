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
from invana_engine.utils import get_field_names
from invana_engine.data_types import NodeType, EdgeType
from .constants import FIELD_TYPES_MAP, WHERE_CONDITIONS_BASE, WHERE_CONDITIONS_DATATYPE_MAP, \
    WHERE_CONDITIONS_FOR_STRING, DEFAULT_LIMIT_SIZE, ALL_WHERE_CONDITIONS, WHERE_CONDITIONS_BOOLEAN


class DynamicSchemaGenerator:

    def __init__(self, schema_data, search_type, is_global_search=False):
        # data_type: node, edge
        if search_type not in ["node", "edge"]:
            raise Exception(f"search_type can only be node or edge. received {search_type}")
        self.schema_data = schema_data
        self.search_type = search_type
        self.is_global_search = is_global_search

    def get_search_type(self):
        return NodeType if self.search_type == "node" else EdgeType

    def create_resolver(self, record_name, record_cls):
        search_type = self.search_type
        is_global_search = self.is_global_search

        def resolver_func(self, info: graphene.ResolveInfo,
                          _limit: int = None,
                          _offset: int = None,
                          _order_by=None,
                          _where=None,
                          _dedup=None
                          ):

            search_kwargs = {}
            fields = get_field_names(info)
            if is_global_search is not True:
                search_kwargs = {"has__label": fields['label']}

            if _where:
                for property_key, where_item in _where.items():
                    if where_item:
                        for predicate_key, predicate_value in where_item.items():
                            search_kwargs[f'has__{property_key}__{predicate_key}'] = predicate_value
            if search_type == "node":
                qs = info.context['request'].app.state.graph.vertex.search(**search_kwargs)
            elif search_type == "edge":
                qs = info.context['request'].app.state.graph.edge.search(**search_kwargs)
            else:
                raise NotImplementedError()
            if _order_by:
                for order_key, order_value in _order_by.items():
                    order_value = order_value.lower()
                    order_key = f"-{order_key}" if order_value == "desc" else order_key
                    qs = qs.order_by(order_key)
            qs = qs.get_traversal()
            if _limit and _offset:
                qs = qs.range(_offset, _offset + _limit)
            elif _limit and not _offset:
                qs = qs.limit(_limit)

            qs = qs.elementMap(*fields['properties'])
            if _dedup is True:
                qs = qs.dedup()
            result = qs.toList()
            data = [d.to_json() for d in result]
            return data

        resolver_func.__name__ = 'resolve_%s' % record_name
        return resolver_func

    def create_record_type(self, classname, properties):
        if properties.values().__len__() > 0:
            record_property_objects_type = type(
                f"{classname}Properties",
                (graphene.ObjectType,),
                properties
            )
            record_extra_fields = {"properties": graphene.Field(record_property_objects_type)}
        else:
            record_extra_fields = {}
        record_type = type(
            f"{classname}{self.search_type.capitalize()}Type",
            (self.get_search_type(),),
            record_extra_fields
        )
        return record_type

    def create_order_by_fields(self, record_class, property_objects):
        order_by_fields = {}
        for property_object in property_objects:
            order_by_fields[property_object['id']] = graphene.String()
        return type(
            f"{record_class.__name__}OrderBy",
            (graphene.InputObjectType,),
            order_by_fields
        )

    def create_where_fields(self, record_class, property_objects):

        node_type_where_filters = {}
        for property_object in property_objects:
            where_filter_fields = {}
            allowed_where_conditions = {}  # based on data type
            # print("=====property_object['type']", property_object['type'])
            if property_object['type'] in ["Integer", "Float", "DateTime"]:
                allowed_where_conditions.update(WHERE_CONDITIONS_BASE)
            elif property_object['type'] in ["Boolean"]:
                allowed_where_conditions.update(WHERE_CONDITIONS_BOOLEAN)
            elif property_object['type'] in ['String', 'Geoshape']:
                allowed_where_conditions.update(ALL_WHERE_CONDITIONS)
            else:
                allowed_where_conditions.update(ALL_WHERE_CONDITIONS)
            for where_condition_key, where_condition_type in allowed_where_conditions.items():
                where_filter_fields[where_condition_key] = where_condition_type()

            property_where_filters = type(
                f"{property_object['type']}_where_filters".lower(),
                (graphene.InputObjectType,),
                where_filter_fields
            )
            node_type_where_filters[property_object['id']] = graphene.Field(property_where_filters)

        ## for global search
        # if self.is_global_search:
        #     node_type_where_filters["label"] = graphene.Field(graphene.List(where_filters))
        # node_type_where_filters["_id"] = graphene.Field(graphene.List(where_filters))

        return type(
            f"{record_class.__name__}_where_filters",
            (graphene.InputObjectType,),
            node_type_where_filters
        )

    def create_record_fields(self, record_class, property_objects):
        extra_fields = {}
        # print("create_record_fields", record_class)
        if property_objects.__len__() > 0:
            extra_fields['_dedup'] = graphene.Argument(graphene.Boolean, default_value=True,
                                                       description="dedup the data")

            order_by_type = self.create_order_by_fields(record_class, property_objects)
            extra_fields['_order_by'] = graphene.Argument(order_by_type,
                                                          description="order_by")

            where_filters = self.create_where_fields(record_class, property_objects)
            extra_fields['_where'] = graphene.Argument(where_filters,
                                                       description="where")
        return graphene.Field(
            graphene.List(record_class),
            _limit=graphene.Argument(graphene.Int, default_value=DEFAULT_LIMIT_SIZE,
                                     required=True, description="limits the result count"),
            _offset=graphene.Argument(graphene.Int, default_value=0,
                                      description="limits the count"),
            **extra_fields
        )

    def create_schema_dynamically(self):
        record_schemas = {}
        record_property_objects = {}
        for record_type in self.schema_data:
            classname = record_type["id"]  # 'Author'
            properties = {}
            record_property_objects[record_type['id']] = []
            for option in record_type["options"]:
                field_type = FIELD_TYPES_MAP[option['type']]
                properties[option['id']] = field_type()  # maybe add label as description
                record_property_objects[record_type['id']].append(option)
            record_schemas[record_type['id']] = self.create_record_type(
                classname,
                properties
            )
        # create Query in similar way
        record_fields = {}
        for key, rec in record_schemas.items():
            record_fields[key] = self.create_record_fields(rec, record_property_objects[key])  # graphene.Field(rec)
            record_fields['resolve_%s' % key] = self.create_resolver(key, rec)
        Query = type(f'{self.search_type}Query'.capitalize(), (graphene.ObjectType,), record_fields)
        record_schema_types = list(record_schemas.values())
        return Query, record_schema_types
