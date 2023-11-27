import graphene
import typing
from .dataclasses import RelationshipField, NodeSchema, RelationshipSchema, \
    PropertyField, GraphSchema



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

class GeneratorBase:

    # @property
    # def graph_schema(self) -> GraphSchema:
    #     if getattr(self, "node_schema"):
    #         return self.node_schema.schema
    #     elif getattr(self, "relationship_schema"):
    #         return self.relationship_schema.schema
    #     return 

    def create_where_order_by(self, type_defs: typing.List[NodeSchema]):
        # create order by 
        order_by_fields = {}
        for type_def in type_defs:
            for field_name, field in type_def.data_fields.items():
                order_by_fields[field_name] = OrderByEnum()
        return type(f"{''.join([type_def.label for type_def in type_defs])}OrderBy", (graphene.InputObjectType, ), order_by_fields)
    

    def _create_where_relationship_condition(self, relationship_label, direction, ):
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
                cls = self._create_where_relationship_condition(
                        field.other_node_label,
                        field.direction,
                    )
                where_condition_fields[f"{field.relationship_label}__{field.other_node_label}"] = cls()

        # traversals 
        return type(f"{type_defs_label}WhereConditions",(graphene.InputObjectType,), where_condition_fields)
 
    def create_property_field(self, field: PropertyField):
        field_str = field.field_type_str
        return getattr(graphene, field_str)()# TODO - add default etc kwargs from ariadne type object
    
    def create_node_type_args(self, type_defs: typing.List[NodeSchema] ):
        return {
            "limit" : graphene.Argument(graphene.Int, description="limits the result count"),
            "offset" : graphene.Argument(graphene.Int, description="skips x results"),
            "dedup" : graphene.Argument(graphene.Boolean, description="dedups the result"),
            "order_by" : graphene.Argument(self.create_where_order_by(type_defs),
                                            description="order the result by"),
            "where": graphene.Argument(self.create_where_conditions(type_defs))
        }
    

class NodeGenerator(GeneratorBase):

    def __init__(self, node_schema: NodeSchema) -> None:
        self.node_schema = node_schema

    def create_relationship_fields_for_node(self, 
                    type_def: NodeSchema,
                    relationships_grouped: typing.Dict[str, typing.List[RelationshipField]]):
        """_summary_

        Args:
            type_def (NodeSchema): node for which relationship fields are being created 
            relationships_grouped (typing.Dict[str, typing.List[RelationshipField]]): _description_

        Returns:
            _type_: _description_
        """
        node_type_fields = {}
 
        for field_name, relationship_fields in relationships_grouped.items():
            fields = {}
            # TODO - add edge properties
            target_label_type_defs = [] # relation going to which Node
            # making relationship_fields list if it is a single relation
            relationship_fields =  [relationship_fields] if type(relationship_fields) is not list else relationship_fields
            for relationship_field in relationship_fields:
                if self.graph_schema.get_node_schema(relationship_field.other_node_label) not in target_label_type_defs:
                    target_label_type_defs.append(self.graph_schema.get_node_schema(relationship_field.other_node_label))
                fields[relationship_field.other_node_label] = self.create_node_type_search_field(
                    self.graph_schema.get_node_schema(relationship_field.other_node_label)
                )
                # TODO - add resolver if needed; fields[f'resolve_{relationship_directive.node_label}'] = resolve_relationship_field_resolver
            object_type = type(f"{type_def.label}{field_name}", (graphene.ObjectType, ), fields) 
            node_type_fields[field_name] =  graphene.Field(graphene.List(object_type),
                                        args=self.create_node_type_args(target_label_type_defs))
        return node_type_fields

    def create_node_data_type_fields(self, type_def: NodeSchema, extra_fields=None):
        # create node type fields
        fields = {}
        # data_fields = type_def.get_data_fields()

        # 1. create actual fields 
        for field_name, field in type_def.data_fields.items():
            fields['id'] = graphene.ID()
            fields['label'] = graphene.String(default_value=type_def.label)
            fields[field_name] = self.create_property_field(field)

        # 2. create relationship fields
        relationship_fields = {}

        # 2.0 actual fields defined in the graphql definition
        relationship_fields.update(type_def.relationship_fields)
        
        # 2.1. inidividual directions
        # there is no bothe for this case, # TODO - may be add bothe if there relationship exits both ways  
        # direction relationship to node ex: "oute__related_to__Node"
        relationship_fields.update(type_def.directed_relationship_to_node("both"))

        # 2.2. relationships grouped by direction and edge label
        #  ex: "ine__related_to", 
        relationship_fields.update(type_def.directed_relationships_grouped_by_edge_label("in"))
        #  ex: "oute__related_to", 
        relationship_fields.update(type_def.directed_relationships_grouped_by_edge_label("out"))
        #  ex: "bothe__related_to", 
        relationship_fields.update(type_def.directed_relationships_grouped_by_edge_label("both"))

        # 2.3. relationships grouped by the direction
        # ex: "ine"
        relationship_fields.update(type_def.generic_directed_relationships("in"))
        # ex: "oute"
        relationship_fields.update(type_def.generic_directed_relationships("out"))
        # ex: "bothe"
        relationship_fields.update(type_def.generic_directed_relationships("both"))

        # create fields         
        fields.update(
            self.create_relationship_fields_for_node(
                type_def,
                relationship_fields
            )
        )

        if extra_fields:
            fields.update(extra_fields)
        return fields

    def create_node_data_type(self, type_def: NodeSchema, extra_fields=None):
        node_type_fields = self.create_node_data_type_fields(type_def, extra_fields=extra_fields)
        return  type(type_def.label, (graphene.ObjectType, ), node_type_fields)

    def create_node_type_search_field(self, type_def: NodeSchema, extra_args=None ):
        NodeDataType = self.create_node_data_type(type_def)
        args =  self.create_node_type_args([type_def])
        if extra_args:
            args.update(extra_args)
        return graphene.Field(graphene.List(NodeDataType), args=args, description=f"Search {type_def.label} node ")


class RelationshipGenerator(GeneratorBase):

    def __init__(self, relationship_schema: RelationshipSchema) -> None:
        self.relationship_schema = relationship_schema

    def create_relationship_data_type(self, type_def: RelationshipSchema, extra_fields=None):
        relationship_type_fields = self.create_relationship_data_type_fields(type_def, extra_fields=extra_fields)
        return  type(type_def.label, (graphene.ObjectType, ), relationship_type_fields)

    def create_relationship_data_type_fields(self, type_def: RelationshipSchema,  extra_fields=None):
        fields = {}
        # data_fields = type_def.get_data_fields()

        # 1. create actual fields 
        for field_name, field in type_def.data_fields.items():
            fields['id'] = graphene.ID()
            fields['label'] = graphene.String(default_value=type_def.label)
            fields[field_name] = self.create_property_field(field)
        
        if extra_fields:
            fields.update(extra_fields)
        return fields
    