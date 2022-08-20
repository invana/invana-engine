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
from invana_engine.utils import get_field_names_from_resolver_info
from invana_engine.data_types import NodeType, EdgeType
from .constants import FIELD_TYPES_MAP, WHERE_CONDITIONS_BASE, WHERE_CONDITIONS_DATATYPE_MAP, \
    WHERE_CONDITIONS_FOR_STRING, DEFAULT_LIMIT_SIZE, ALL_WHERE_CONDITIONS, WHERE_CONDITIONS_BOOLEAN


# from .store import TypeStore
# from .utils import convert_to_graphql_schema
# from ..graph.query import GraphSchema
# from ..modeller.query import ModellerQuery


class Helpers:

    def create_schema_type(self, ):
        pass


class DynamicSchemaGenerator:

    def __init__(self, schema_store):
        # self.type_store = TypeStore()
        # self.schema_data = schema_data
        # self.search_type = search_type
        # self.is_global_search = is_global_search

        self.schema_store = schema_store
        self.record_schema_property_objects = {}
        self.node_record_schemas = {}
        self.edge_record_schemas = {}
        self.node_label_fields = {}  # this includes id, _where, _limit, _traverse fields
        self.edge_label_fields = {}  # this includes id, _where, _limit, _traverse fields

    @staticmethod
    def get_record_response_type(search_type):
        return NodeType if search_type == "node" else EdgeType

    def create_resolver(self, record_name, record_cls, search_type):
        # is_global_search = self.is_global_search

        def resolver_func(self,
                          info: graphene.ResolveInfo,
                          _limit: int = None,
                          _offset: int = None,
                          _order_by=None,
                          _where=None,
                          _dedup=None
                          ):

            search_kwargs = {}
            fields = get_field_names_from_resolver_info(info)
            if fields['label']:
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

    def create_record_type(self, search_type, classname, properties):
        if properties.values().__len__() > 0:
            record_schema_property_objects_type = type(
                f"{classname}Properties",
                (graphene.ObjectType,),
                properties
            )
            record_extra_fields = {"properties": graphene.Field(record_schema_property_objects_type)}
        else:
            record_extra_fields = {}
        record_type = type(
            f"{classname}{search_type.capitalize()}Type",
            (self.get_record_response_type(search_type),),  # extending NodeType/EdgeType
            record_extra_fields
        )
        return record_type

    def create_order_by_fields(self, record_class, property_objects):
        order_by_fields = {}
        for property_object in property_objects:
            order_by_fields[property_object['id']] = graphene.String()

        id_where_filter_fields = self.create_filters_based_on_datatype("String")
        id_property_order_by_filter = self.create_where_filter_object_type("id", id_where_filter_fields)
        order_by_fields["_id"] = self.create_filters_based_on_datatype("String") #graphene.Field(id_property_order_by_filter)

        return type(
            f"{record_class.__name__}OrderBy",
            (graphene.InputObjectType,),
            order_by_fields
        )

    def create_filters_based_on_datatype(self, data_type):
        where_filter_fields = {}
        allowed_where_conditions = {}  # based on data type
        # print("=====property_object['type']", property_object['type'])
        if data_type in ["Integer", "Float", "DateTime"]:
            allowed_where_conditions.update(WHERE_CONDITIONS_BASE)
        elif data_type in ["Boolean"]:
            allowed_where_conditions.update(WHERE_CONDITIONS_BOOLEAN)
        elif data_type in ['String', 'Geoshape']:
            allowed_where_conditions.update(ALL_WHERE_CONDITIONS)
        else:
            allowed_where_conditions.update(ALL_WHERE_CONDITIONS)
        for where_condition_key, where_condition_type in allowed_where_conditions.items():
            where_filter_fields[where_condition_key] = where_condition_type()
        return where_filter_fields

    def create_where_filter_object_type(self, object_name, filter_fields):
        # TODO - register this to a cache
        return type(
            f"{object_name}WhereFilters".lower(),
            (graphene.InputObjectType,),
            filter_fields
        )

    def create_edge_filters(self, parent_node_label, edge_label, edge_type):
        return graphene.Field(type(
            f"{parent_node_label}_{edge_type}_{edge_label}_query",
            (graphene.InputObjectType,),
            self.edge_label_fields[edge_label].args
        ))

    def create_where_fields(self, record_class, property_objects):

        node_type_where_filters = {}
        for property_object in property_objects:
            where_filter_fields = self.create_filters_based_on_datatype(property_object['type'])
            property_where_filters = self.create_where_filter_object_type(
                property_object['type'], where_filter_fields
            )
            node_type_where_filters[property_object['id']] = graphene.Field(property_where_filters)

        # TODO - add _id filter

        id_where_filter_fields = self.create_filters_based_on_datatype("String")
        id_property_where_filters = self.create_where_filter_object_type("id", id_where_filter_fields)
        node_type_where_filters["_id"] = graphene.Field(id_property_where_filters)

        # TODO - get the _oute_ and _ine_ labels

        is_node = True if "NodeType" in str(record_class) else False
        # print("is_node", is_node, "=======", record_class)
        # TOD now detect the ine and oute from this node

        if is_node:
            pass
            # detect in and out edges
            node_label = str(record_class).replace("NodeType", "")
            for label in self.schema_store.vertex__edges_map[f"{node_label}__ine"]:
                search_type = "edge"
                # create if not exist
                self.create_and_register_record_type_if_not_exist(self.schema_store.edge_schema_gql_map[label],
                                                                  search_type)
                self.create_label_fields_of_search_type(search_type)
                node_type_where_filters[f"ine__{label}"] = self.create_edge_filters(node_label, label, "ine")

            for label in self.schema_store.vertex__edges_map[f"{node_label}__oute"]:
                search_type = "edge"
                self.create_and_register_record_type_if_not_exist(self.schema_store.edge_schema_gql_map[label],
                                                                  search_type)
                self.create_label_fields_of_search_type(search_type)
                node_type_where_filters[f"oute__{label}"] = self.create_edge_filters(node_label, label, "oute")

        else:
            pass
 
        # TODO -
        # print("record_class", record_class, self.schema_store)

        ## for global search
        # if self.is_global_search:
        #     node_type_where_filters["label"] = graphene.Field(graphene.List(where_filters))
        # node_type_where_filters["_id"] = graphene.Field(graphene.List(where_filters))

        return type(
            f"{record_class.__name__}WhereFilters",
            (graphene.InputObjectType,),
            node_type_where_filters
        )

    def create_label_field_args(self, record_class, property_objects):
        fields = {}
        # print("create_label_fields", record_class)
        # if property_objects.__len__() > 0:
        fields['_dedup'] = graphene.Argument(graphene.Boolean, default_value=True,
                                             description="dedup the data")

        order_by_type = self.create_order_by_fields(record_class, property_objects)
        fields['_order_by'] = graphene.Argument(order_by_type,
                                                description="order_by")

        where_filters = self.create_where_fields(record_class, property_objects)
        fields['_where'] = graphene.Argument(where_filters,
                                             description="to filter the data")

        fields['_limit'] = graphene.Argument(graphene.Int, default_value=DEFAULT_LIMIT_SIZE,
                                             required=True, description="limits the result count")
        fields['_offset'] = graphene.Argument(graphene.Int, default_value=0,
                                              description="limits the count")
        return fields

    def create_label_fields(self, record_class, property_objects):
        return self.create_label_field_args(record_class, property_objects)
        # return graphene.Field(graphene.List(record_class), **fields)

    def create_and_register_record_type_if_not_exist(self, record_schema, search_type):
        # this will register label data type # id, label, type, properties.name, properties.age ... so on.
        classname = record_schema["id"]  # 'Author'
        record_schemas = self.node_record_schemas if search_type == "node" else self.edge_record_schemas
        if record_schema['id'] in record_schemas:
            # check if schema is already registered,
            # if yes do nothing
            # else create record schema and register it to inmemory dict
            return

        properties = {}
        self.record_schema_property_objects[record_schema['id']] = []
        for option in record_schema["options"]:
            field_type = FIELD_TYPES_MAP[option['type']]
            properties[option['id']] = field_type()  # maybe add label as description
            self.record_schema_property_objects[record_schema['id']].append(option)

        # register here to in memory store
        if search_type == "node":
            self.node_record_schemas[record_schema['id']] = self.create_record_type(
                search_type,
                classname,
                properties
            )
        elif search_type == "edge":
            self.edge_record_schemas[record_schema['id']] = self.create_record_type(
                search_type,
                classname,
                properties
            )
        else:
            raise Exception("search_type should be either node or edge")

    def get_record_schemas_of_search_type(self, search_type):
        return self.node_record_schemas if search_type == "node" else self.edge_record_schemas

    def create_label_fields_of_search_type(self, search_type):
        # create Query in similar way
        # label_fields = {}
        record_schemas = self.get_record_schemas_of_search_type(search_type)
        for key, record_class in record_schemas.items():
            fields = self.create_label_fields(record_class, self.record_schema_property_objects[key])
            field_resolver = self.create_resolver(key, record_class, search_type)

            record_field = graphene.Field(graphene.List(record_class), fields)
            if search_type == "node":
                self.node_label_fields[key] = record_field
                self.node_label_fields['resolve_%s' % key] = field_resolver
            elif search_type == "edge":
                self.edge_label_fields[key] = record_field
                self.edge_label_fields['resolve_%s' % key] = field_resolver
        # return label_fields

    # def create_label_fields_of_label(self, record, )

    def create_schema_dynamically(self, *extra_schema_types):
        types = []
        query_schemas = []
        for search_type in ["node", "edge"]:
            # create node types
            schema_gql_map = self.schema_store.vertex_schema_gql_map if search_type == "node" else \
                self.schema_store.edge_schema_gql_map
            for label, record_schema in schema_gql_map.items():
                self.create_and_register_record_type_if_not_exist(record_schema, search_type)

            self.create_label_fields_of_search_type(search_type)
            label_fields = self.node_label_fields if search_type == "node" else self.edge_label_fields
            SearchTypeQuery = type(f'{search_type}Query'.capitalize(), (graphene.ObjectType,), label_fields)
            query_schemas.append(SearchTypeQuery)

            record_schemas = self.get_record_schemas_of_search_type(search_type)
            types.extend(list(record_schemas.values()))

        # return Query, record_schema_types
        # class Query(ModellerQuery, GraphSchema, *query_schemas):
        #     pass

        class Query(*extra_schema_types, *query_schemas):
            pass

        return graphene.Schema(query=Query,
                               types=types,
                               # + vertex_search_record_schema_types + edge_search_record_schema_types,
                               auto_camelcase=False
                               )
