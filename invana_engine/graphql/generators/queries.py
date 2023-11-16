import graphene
from .types import InvanaGQLFieldRelationshipDirective, InvanaGQLLabelDefinition, \
    InvanaGQLLabelDefinitionField, InvanaGQLSchema
from .exceptions import UnSupportedFieldDirective
import typing

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


class QueryGenerators:
 
    def __init__(self,   schema_defs: InvanaGQLSchema) -> None:
        self.schema_defs = schema_defs
        # self.label_def = label_def
        # self.type_name = label_def.label
        self.schema_types_dict = {"nodes": {}, "relationships": {}}

    def get_type_from_schema_cache(self, type_def: InvanaGQLLabelDefinition ):
        if type_def.label_type == "relationship":
            return self.schema_types_dict['relationships'].get(type_def.label)
        elif type_def.label_type == "node":
            return self.schema_types_dict['nodes'].get(type_def.label)

    def add_type_to_schema_cache(self, type_def: InvanaGQLLabelDefinition, _type: graphene.ObjectType):
        if type_def.label_type == "relationship":
            self.schema_types_dict['relationships'][type_def.label] = _type
        elif type_def.label_type == "node":
            self.schema_types_dict['nodes'][type_def.label] = _type

    def create_field(self, field: InvanaGQLLabelDefinitionField):
        field_str = field.field_type_str
        return getattr(graphene, field_str)()# TODO - add default etc kwargs from ariadne type object
    
    # def create_relationship_field(self, directive):
    #     # dummy
    #     NodeType =  type(directive['node_label'], (graphene.ObjectType, ), {})
    #     return graphene.Field(graphene.List(NodeType)) 
    

    # def create_relationship_based_fields(self, 
    #             directive: InvanaGQLFieldRelationshipDirective,
    #             type_def: InvanaGQLLabelDefinition
    #             ):
       
    #     # related_fields = type_def.get_related_fields()
    #     # create relationship field -> returns edges data
    #     # create in_relationship__Node field -> returns nodes data 
    #     relation_based_fields = {}
    #     # for direction, field in related_fields.items():

    #     # traverse on just relationships -> returns edges data
    #     relation_prefix = f"{directive.direction}__".lower()
    #     relation_based_fields[f"{relation_prefix}{directive.relationship_label}"] = \
    #                                 graphene.Field(graphene.List(
    #                                     type(directive.node_label, (graphene.ObjectType, ), {})
    #                                 )) 

    #     # traverse via relationships to Nodes -> returns related nodes data 
    #     relation_based_fields[f"{relation_prefix}{directive.relationship_label}__{directive.node_label}"] = graphene.Field(graphene.List(
    #         type(directive.node_label, (graphene.ObjectType, ), {})
    #     )) 
    #     # TODO - add 
    #     return relation_based_fields


    def create_relationship_fields(self,  relationship_directives: typing.List[InvanaGQLFieldRelationshipDirective]):    
        classes = [type(relationship_directive.node_label, (graphene.ObjectType, ), {}) 
                   for relationship_directive in relationship_directives]    
        return graphene.Field(graphene.List(*classes)) 
        
    def create_node_type(self, type_def: InvanaGQLLabelDefinition):
 
        # create node type
        node_type_fields = {}
        
        data_fields = type_def.get_data_fields()

        # 1. create actual fields 
        for field_name, field in data_fields.items():
            node_type_fields['id'] = graphene.ID()
            node_type_fields['label'] = graphene.String()
            node_type_fields[field_name] = self.create_field(field)

        # 2. create relationship fields
 
        related_fields = type_def.get_related_fields()
        for field_name, relationship_directives in related_fields.items():
            node_type_fields[field_name] = self.create_relationship_fields(relationship_directives)


        NodeType =  type(type_def.label, (graphene.ObjectType, ), node_type_fields)
        self.add_type_to_schema_cache(type_def, NodeType)
        return NodeType


    # def create_relationship_type(self, type_def: InvanaGQLLabelDefinition):
    #     # create node type
    #     node_type_fields = {}

    #     for field_name, field in type_def.fields.items():
    #         node_type_fields['_id'] = graphene.ID()
    #         node_type_fields['_label'] = graphene.String()
    #         if list(field.directives.keys()).__len__() ==  0:
    #             # this is property on the node
    #             node_type_fields[field_name] = self.create_field(field)
    #         else: # this is a relationship on the if directive_name == "relationship"
    #             for directive_name, directive in field.directives.items():
    #                 if directive_name == "relationship":
    #                     relationship_based_fields = self.create_relationship_based_fields(directive_name, directive)
    #                     for related_name, related_field,  in relationship_based_fields.items():
    #                         node_type_fields[related_name] = related_field
    #                 else:
    #                     raise UnSupportedFieldDirective(f"'{directive_name}' directive is not supported on the field")
    #     NodeType =  type(type_def.label, (graphene.ObjectType, ), node_type_fields)
    #     self.add_type_to_schema_cache(type_def, NodeType)
    #     return NodeType



    def create_order_by(self, type_def: InvanaGQLLabelDefinition):
        # create order by 
        order_by_fields = {}
        for field_name, field in type_def.fields.items():
            order_by_fields[field_name] = OrderByEnum()
        return type(f"{type_def.label}OrderBy", (graphene.InputObjectType, ), order_by_fields)
    
    def create_relationship_field_name(self, directive):
        return f"{directive.relationship_label}__{directive.node_label}"
    
    def create_where_relationship_condition(self, relationship_label, direction, ):
        return type(f"{relationship_label}WhereConditions", (graphene.InputObjectType, ), {
            "id": graphene.String()
        })

    def create_where_conditions(self, type_def: InvanaGQLLabelDefinition):
        """
        """
        # create where 
        """
        NodeWhereConditions2 is a hack to avoid the error 
        `UnboundLocalError: local variable 'NodeWhereConditions' referenced before assignment`"""
        NodeWhereConditions2 = type(f"{type_def.label}WhereConditions",(graphene.InputObjectType, ),{})
        where_condition_fields = {     
            "_and": NodeWhereConditions2(),
            "_or": NodeWhereConditions2(),
            "_not": NodeWhereConditions2()
        }
        # fields
        for field_name, field in type_def.fields.items():
            if list(field.directives.keys()).__len__() >  0:
                for directive_name, directive_data in field.directives.items():
                    if directive_name == "relationship":
                        cls = self.create_where_relationship_condition(
                                directive_data.node_label,
                                directive_data.direction,
                            )
                        where_condition_fields[self.create_relationship_field_name(directive_data)] = cls()
            elif field.field_type_str == "String":
                where_condition_fields[field_name] = StringFilersExpressions()
            elif field.field_type_str == "Int":
                where_condition_fields[field_name] = IntFilersExpressions()

        # traversals 
        return type(f"{type_def.label}WhereConditions",(graphene.InputObjectType,), where_condition_fields)

    def generate_query_object_type_with_filters(self, type_def: InvanaGQLLabelDefinition):

        def resolve_query(self, info: graphene.ResolveInfo, **kwargs):
            return [{
                "id": "op",
                "first_name": "my name is good",
                "email": "me@gmail.com",
                "authored_project":[
                    {
                        "_id": '1',
                        "_label": "RelLabel",
                        "description": "Hello world"
                    }
                ]

            }]

        NodeType = self.get_type_from_schema_cache(type_def)

        if type_def.label_type == "node":
            NodeType = self.create_node_type(type_def) if NodeType is None else NodeType
        elif type_def.label_type == "relationship":
            NodeType = self.create_node_type(type_def) if NodeType is None else NodeType


        NodeOrderBy = self.create_order_by(type_def)
        NodeWhereConditions = self.create_where_conditions(type_def)

        LabelQueryTypes  = type(type_def.label, (graphene.ObjectType, ), {
            type_def.label : graphene.Field(graphene.List(NodeType), args={
                "limit" : graphene.Argument(graphene.Int, description="limits the result count"),
                "offset" : graphene.Argument(graphene.Int, description="skips x results"),
                "dedup" : graphene.Argument(graphene.Boolean, description="dedups the result"),
                "order_by" : graphene.Argument(NodeOrderBy , description="order the result by"),
                "where": graphene.Argument(NodeWhereConditions)
            }),
            f"resolve_{type_def.label}" : resolve_query
        })
        return LabelQueryTypes

    def generate(self):
        #  type_def: InvanaGQLLabelDefinition,
        query_classes = []

        for type_name, type_def in self.schema_defs.nodes.items():
            LabelQueryTypes = self.generate_query_object_type_with_filters(type_def)
            query_classes.append(LabelQueryTypes)         

        for type_name, type_def in self.schema_defs.relationships.items():
            LabelQueryTypes = self.generate_query_object_type_with_filters(type_def)
            query_classes.append(LabelQueryTypes)         
            
        return query_classes



