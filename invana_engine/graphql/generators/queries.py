import graphene
from .types import InvanaGQLFieldRelationshipDirective, InvanaGQLLabelDefinition, \
    InvanaGQLLabelFieldDefinition, InvanaGQLSchema
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


class CacheManager:
    
    # node: typing.Dict[str, typing.Tuple(graphene.ObjectType,   )]
    def __init__(self) -> None:
        self.node_types = {}
        self.rel_types = {}


class QueryGenerators:
 
    def __init__(self,   schema_defs: InvanaGQLSchema) -> None:
        self.schema_defs = schema_defs
        # self.label_def = label_def
        # self.type_name = label_def.label
        self.schema_types_dict = {"nodes": {}, "relationships": {}}

    def get_type_from_schema_cache(self, label: str, label_type: str )->  InvanaGQLLabelDefinition:
        if label_type == "relationship":
            return self.schema_types_dict['relationships'].get(label)
        elif label_type == "node":
            return self.schema_types_dict['nodes'].get(label)

    def add_type_to_schema_cache(self, 
                type_def: InvanaGQLLabelDefinition, 
                _type: graphene.ObjectType):
        if type_def.label_type == "relationship":
            self.schema_types_dict['relationships'][type_def.label] = _type
        elif type_def.label_type == "node":
            self.schema_types_dict['nodes'][type_def.label] = _type

    def create_field(self, field: InvanaGQLLabelFieldDefinition):
        field_str = field.field_type_str
        return getattr(graphene, field_str)()# TODO - add default etc kwargs from ariadne type object
 
    def create_node_with_name(self, node_name):
        # TODO - get from cached
        type_def = self.schema_defs.nodes[node_name]
        LabelQueryTypes = self.create_node_object_type_with_filters(type_def)
        return LabelQueryTypes
        # return self.get_type_from_schema_cache(node_name, "node")
        # return type(node_name, (graphene.ObjectType, ), {}) 

    def create_node_relationship_field(self, 
            type_def_label: str,
            field_name:str, 
            relationship_directives: typing.List[InvanaGQLFieldRelationshipDirective]
        ):
        fields = {}

        if field_name.split("__").__len__() == 3:
            # individual relation to node map; "_oute__ACTED_IN__Movie"
            for relationship_directive in relationship_directives:
                fields[relationship_directive.field_name] = graphene.Field(
                    graphene.List(self.create_node_with_name(relationship_directive.node_label))
                )
                def resolve_query(self, info: graphene.ResolveInfo, **kwargs):
                    return []
                fields[f'resolve_{relationship_directive.field_name}'] = resolve_query

            object_type = type(relationship_directive.node_label, (graphene.ObjectType, ), fields) 
        elif field_name.split("__").__len__() == 2:
            # individual relation to node map # "_oute__ACTED_IN"
            for relationship_directive in relationship_directives:
                fields[relationship_directive.field_name] = graphene.Field(
                    graphene.List(self.create_node_with_name(relationship_directive.node_label))
                )
                def resolve_query(self, info: graphene.ResolveInfo, **kwargs):
                    return []
                fields[f'resolve_{relationship_directive.field_name}'] = resolve_query

            # TODO - add filters
            object_type = type(f"{type_def_label}{field_name}", (graphene.ObjectType, ), fields) 
        elif field_name in ["_bothe", "_ine", "_oute"]:
            # add traversal
            for relationship_directive in relationship_directives:
                fields[relationship_directive.field_name] = graphene.Field(
                    graphene.List(self.create_node_with_name(relationship_directive.node_label))
                )
                def resolve_query(self, info: graphene.ResolveInfo, **kwargs):
                    return []
                fields[f'resolve_{relationship_directive.field_name}'] = resolve_query

            # TODO - add filters
            object_type = type(f"{type_def_label}{field_name}", (graphene.ObjectType, ), fields) 
        return graphene.Field(graphene.List(object_type)) 
 
 

        # return graphene.Field(graphene.List(*object_type)) 
        
    def create_node_type(self, type_def: InvanaGQLLabelDefinition, extra_fields=None):
 
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
            node_type_fields[field_name] = self.create_node_relationship_field(
                type_def.label,
                field_name, relationship_directives)


        NodeType =  type(type_def.label, (graphene.ObjectType, ), node_type_fields)
        self.add_type_to_schema_cache(type_def, NodeType) # add to cache 
        return NodeType

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

    def create_node_object_type_with_filters(self, 
            type_def: InvanaGQLLabelDefinition,
            extra_fields=None):

        # create Object Type
        NodeType = self.get_type_from_schema_cache(type_def.label, type_def.label_type)
        NodeType = self.create_node_type(type_def) if NodeType is None else NodeType

        # create fields 
        node_fields = {}
        def resolve_query(self, info: graphene.ResolveInfo, **kwargs):
            return []
        node_fields[type_def.label] =  graphene.Field(graphene.List(NodeType), args= {
                "limit" : graphene.Argument(graphene.Int, description="limits the result count"),
                "offset" : graphene.Argument(graphene.Int, description="skips x results"),
                "dedup" : graphene.Argument(graphene.Boolean, description="dedups the result"),
                "order_by" : graphene.Argument(self.create_order_by(type_def) , description="order the result by"),
                "where": graphene.Argument(self.create_where_conditions(type_def))
        })
        node_fields[f"resolve_{type_def.label}"]  = resolve_query

        LabelQueryTypes  = type(type_def.label, (graphene.ObjectType, ), node_fields)
        return LabelQueryTypes

    def generate(self):
        #  type_def: InvanaGQLLabelDefinition,
        query_classes = []

        for type_name, type_def in self.schema_defs.nodes.items():
            LabelQueryTypes = self.create_node_object_type_with_filters(type_def)
            query_classes.append(LabelQueryTypes)         

        for type_name, type_def in self.schema_defs.relationships.items():
            LabelQueryTypes = self.create_node_object_type_with_filters(type_def)
            query_classes.append(LabelQueryTypes)         
            
        return query_classes
 