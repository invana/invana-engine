import graphene
from .gql_types import RelationshipField, NodeSchema, \
    PropertyField, GraphSchema
from .exceptions import UnSupportedFieldDirective
import typing
from .resolvers import default_node_type_search_resolve_query, resolve_relationship_field_resolver,\
    default_node_type_search_by_id_resolve_query

OrderByEnum = type("OrderByEnum", (graphene.Enum, ), {"asc": "asc", "desc": "desc"})

StringFilersExpressions = type("StringFilerExpressions", (graphene.InputObjectType, ), {
    "eq": graphene.String(),
    "in": graphene.List(graphene.String)
})

IntFilersExpressions = type("IntFilersExpressions", (graphene.InputObjectType, ), {
    "eq": graphene.Int(),
    "gt": graphene.Int(),
    "gte": graphene.Int(),
    "lt": graphene.Int(),
    "in": graphene.List(graphene.Int)
})
"""
all the types above are generic reusable
"""


class CacheManager:
    
    # node: typing.Dict[str, typing.Tuple(graphene.ObjectType,   )]
    def __init__(self) -> None:
        self.node_types = {}
        self.rel_types = {}



class QueryGenerators:
 
    def __init__(self, schema_defs: GraphSchema) -> None:
        self.schema_defs = schema_defs
        self.schema_types_dict = {"nodes": {}, "relationships": {}}
 
    def create_where_order_by(self, type_defs: typing.List[NodeSchema]):
        # create order by 
        order_by_fields = {}
        for type_def in type_defs:
            for field_name, field in type_def.data_fields.items():
                order_by_fields[field_name] = OrderByEnum()
        return type(f"{''.join([type_def.label for type_def in type_defs])}OrderBy", (graphene.InputObjectType, ), order_by_fields)
    
    def create_where_relationship_condition(self, relationship_label, direction, ):
        return type(f"{relationship_label}WhereConditions", (graphene.InputObjectType, ), {
            "id": graphene.String()
        })

    def create_where_conditions(self, type_defs: typing.List[NodeSchema]):
        """
        """
        # create where 
        """
        NodeWhereConditions2 is a hack to avoid the error 
        `UnboundLocalError: local variable 'NodeWhereConditions' referenced before assignment`"""
        type_defs_label = ''.join([type_def.label for type_def in type_defs])
        NodeWhereConditions2 = type(f"{type_defs_label}WhereConditions",(graphene.InputObjectType, ),{})
        where_condition_fields = {     
            "_and": NodeWhereConditions2(),
            "_or": NodeWhereConditions2(),
            "_not": NodeWhereConditions2()
        }
        # fields
        for type_def in type_defs:

            for field_name, field in type_def.data_fields.items():
                if field.field_type_str == "String":
                    where_condition_fields[field_name] = StringFilersExpressions()
                elif field.field_type_str == "Int":
                    where_condition_fields[field_name] = IntFilersExpressions()

            for field_name, field in type_def.relationship_fields.items():
                cls = self.create_where_relationship_condition(
                        field.other_node_label,
                        field.direction,
                    )
                where_condition_fields[f"{field.relationship_label}__{field.other_node_label}"] = cls()

        # traversals 
        return type(f"{type_defs_label}WhereConditions",(graphene.InputObjectType,), where_condition_fields)
 
    def create_property_field(self, field: PropertyField):
        field_str = field.field_type_str
        return getattr(graphene, field_str)()# TODO - add default etc kwargs from ariadne type object
 
    def create_relationship_fields_for_grouped_target_nodes(self, 
                    type_def: NodeSchema,
                    relationships_grouped: typing.Dict[str, typing.List[RelationshipField]]):
        node_type_fields = {}
 
        for field_name, relationship_fields in relationships_grouped.items():
            fields = {}
            # TODO - add edge properties
            target_label_type_defs = [] # relation going to which Node
            for relationship_field in relationship_fields:
                if self.schema_defs.nodes[relationship_field.other_node_label] not in target_label_type_defs:
                    target_label_type_defs.append(self.schema_defs.nodes[relationship_field.other_node_label])
                fields[relationship_field.other_node_label] = self.create_node_type_field_by_name(
                    relationship_field.other_node_label
                )
                # TODO - add resolver if needed; fields[f'resolve_{relationship_directive.node_label}'] = resolve_relationship_field_resolver
            object_type = type(f"{type_def.label}{field_name}", (graphene.ObjectType, ), fields) 
            node_type_fields[field_name] =  graphene.Field(graphene.List(object_type),
                                        args=self.create_node_type_args(target_label_type_defs))
        return node_type_fields


    def create_node_data_type_fields(self, type_def: NodeSchema, extra_fields=None):
        # create node type
        node_type_fields = {}
        # data_fields = type_def.get_data_fields()

        # 1. create actual fields 
        for field_name, field in type_def.data_fields.items():
            node_type_fields['id'] = graphene.ID()
            node_type_fields['label'] = graphene.String(default_value=type_def.label)
            node_type_fields[field_name] = self.create_property_field(field)

        # 2. create relationships fields 
        for field_name, field in type_def.relationship_fields.items():
            node_type_fields[field_name] = self.create_node_type_search_field(
                self.schema_defs.nodes[field.other_node_label]
            )

        # 2.1. inidividual directions
        # there is no bothe for this case, # TODO - may be add bothe if there relationship exits both ways  
        # direction relationship to node ex: "oute__related_to__Node"
        for field_name, relationship_field in type_def.directed_relationship_to_node("both").items():
            # target_label = relationship_directives[0].node_label # traverse towards label
            node_type_fields[field_name] = self.create_node_type_search_field(
                self.schema_defs.nodes[relationship_field.other_node_label]
            )
            
        
        # 2.2. relationships grouped by direction and edge label
        #  ex: "bothe__related_to", 
        node_type_fields.update(
            self.create_relationship_fields_for_grouped_target_nodes(
                type_def,
                type_def.directed_relationships_grouped_by_edge_label("both")
            )
        )
        #  ex: "oute__related_to", 
 
        node_type_fields.update(
            self.create_relationship_fields_for_grouped_target_nodes(
                type_def,
                type_def.directed_relationships_grouped_by_edge_label("out")
            )
        )
        #  ex: "ine__related_to", 
        node_type_fields.update(
            self.create_relationship_fields_for_grouped_target_nodes(
                type_def,
                type_def.directed_relationships_grouped_by_edge_label("in")
            )
        )

        # 2.3. relationships grouped by the direction
        # ex: "ine"
        node_type_fields.update(
            self.create_relationship_fields_for_grouped_target_nodes(
                type_def,
                type_def.generic_directed_relationships("in")
            )
        )

        # ex: "oute"
        node_type_fields.update(
            self.create_relationship_fields_for_grouped_target_nodes(
                type_def,
                type_def.generic_directed_relationships("out")
            )
        )

        # ex: "bothe"
        node_type_fields.update(
            self.create_relationship_fields_for_grouped_target_nodes(
                type_def,
                type_def.generic_directed_relationships("both")
            )
        )
                
        if extra_fields:
            node_type_fields.update(extra_fields)
        return node_type_fields

    def create_node_data_type(self, type_def: NodeSchema, extra_fields=None):
        node_type_fields = self.create_node_data_type_fields(type_def, extra_fields=extra_fields)
        return  type(type_def.label, (graphene.ObjectType, ), node_type_fields)

    def create_node_type_args(self, type_defs: typing.List[NodeSchema] ):
        return {
            "limit" : graphene.Argument(graphene.Int, description="limits the result count"),
            "offset" : graphene.Argument(graphene.Int, description="skips x results"),
            "dedup" : graphene.Argument(graphene.Boolean, description="dedups the result"),
            "order_by" : graphene.Argument(self.create_where_order_by(type_defs),
                                            description="order the result by"),
            "where": graphene.Argument(self.create_where_conditions(type_defs))
        }
    
    def create_node_type_search_field(self, type_def: NodeSchema, extra_args=None ):
        NodeDataType = self.create_node_data_type(type_def)
        args =  self.create_node_type_args([type_def])
        if extra_args:
            args.update(extra_args)
        return graphene.Field(graphene.List(NodeDataType), args=args, description=f"Search {type_def.label} node ")

    def create_node_type_field_by_name(self, node_name: str, extra_args=None):
        # TODO - get from cached
        return  self.create_node_type_search_field( self.schema_defs.nodes[node_name], extra_args=extra_args)
 
    def create_node_type_search_field_with_resolver(self, 
                        type_def: NodeSchema,
                        extra_args=None) -> typing.Dict[str, typing.Union[graphene.Field, typing.Callable]]:
        fields = {}
        fields[type_def.label] =  self.create_node_type_search_field(type_def, extra_args=extra_args)
        fields[f"resolve_{type_def.label}"]  = default_node_type_search_resolve_query
        return fields
        
    def create_node_type_search_by_id_field(self, type_def: NodeSchema, extra_args=None ):
        NodeDataType = self.create_node_data_type(type_def)
        args =  {
            'id':  graphene.Argument(graphene.ID, description="id of the node/relationship"),
        }
        if extra_args:
            args.update(extra_args)
        return graphene.Field(NodeDataType, args=args, description=f"Search {type_def.label} by id ")
    
    def create_node_type_search_by_id_field_with_resolver(self, 
                        type_def: NodeSchema,
                        extra_args=None) -> typing.Dict[str, typing.Union[graphene.Field, typing.Callable]]:
        extra_args = {} if extra_args is None else extra_args
        fields = {}
        fields[f'{type_def.label}_by_id'] = self.create_node_type_search_by_id_field(type_def, extra_args=extra_args)
        fields[f"resolve_{type_def.label}_by_id"]  = default_node_type_search_by_id_resolve_query
        return fields
    
    def create_entire_graph_search_with_resolver(self):
        node_fields = {}
        # add over all arguments 
        # add fields
        # where filters
        #        on all fields 
        #        on label_type, labels
        node_fields["_graph"] =  graphene.Field(graphene.List(graphene.String)) # TODO - this is mocked
        node_fields[f"resolve__graph"]  = default_node_type_search_resolve_query
        return node_fields

    def generate(self):
        #  type_def: NodeSchema,
        query_classes = []

        for type_name, type_def in self.schema_defs.nodes.items():
            # label search
            node_fields = self.create_node_type_search_field_with_resolver( type_def)
            query_classes.append(type(type_def.label, (graphene.ObjectType, ), node_fields))         
            # label search by id 
            node_fields = self.create_node_type_search_by_id_field_with_resolver( type_def)
            query_classes.append(type(f'{type_def.label}_by_id', (graphene.ObjectType, ), node_fields))         
 
        # for type_name, type_def in self.schema_defs.relationships.items():
        #     # label search 
        #     node_fields = self.create_node_type_search_field_with_resolver(type_def)
        #     query_classes.append(type(type_def.label, (graphene.ObjectType, ), node_fields))         
        #     # label search by id
        #     node_fields = self.create_node_type_search_by_id_field_with_resolver( type_def)
        #     query_classes.append(type(f'{type_def.label}_by_id', (graphene.ObjectType, ), node_fields))         
 
        node_fields = self.create_entire_graph_search_with_resolver()
        query_classes.append(type("_graph", (graphene.ObjectType, ), node_fields))         

        return query_classes
