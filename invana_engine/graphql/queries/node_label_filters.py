import graphene

"""

"""
OrderByEnum = type("OrderByEnum", (graphene.Enum, ), {"asc": "asc", "desc": "desc"})
StringFilersExpressions = type("StringFilerExpressions", (graphene.InputObjectType, ), {
    "eq": graphene.String(),
    "in": graphene.List(graphene.String),
 
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


def create_field(field):
    field_str = field['field_type_str']
    return getattr(graphene, field_str)()


def create_label_query_type(type_name, type_def_dict):


    # create node type
    node_type_fields = {}
    for field_name, field in type_def_dict['fields'].items():
        if list(field['directives'].keys()).__len__() ==  0:
           node_type_fields[field_name] = create_field(field)
        else:
            pass # process the rel    
    NodeType = type(f"{type_name}", (graphene.ObjectType, ), node_type_fields) 


    # create order by 
    order_by_fields = {}
    for field_name, field in type_def_dict['fields'].items():
        order_by_fields[field_name] = OrderByEnum()
    NodeOrderBy = type(f"{type_name}OrderBy", (graphene.InputObjectType, ), order_by_fields) 

    # create where 
    # NodeWhereConditions2 is a hack to avoid the error 
    # `UnboundLocalError: local variable 'NodeWhereConditions' referenced before assignment`
    NodeWhereConditions2 = type(f"{type_name}WhereConditions",(graphene.InputObjectType, ),{})


    white_condition_fields = {     
        "_and": NodeWhereConditions2(),
        "_or": NodeWhereConditions2(),
        "_not": NodeWhereConditions2()
    }
    for field_name, field in type_def_dict['fields'].items():
        if field['field_type_str'] == "String":
            white_condition_fields[field_name] = StringFilersExpressions()
        elif field['field_type_str'] == "Int":
            white_condition_fields[field_name] = IntFilersExpressions()

    
    NodeWhereConditions = type(f"{type_name}WhereConditions",(graphene.InputObjectType, ),white_condition_fields)

    def resolve_query(self, info: graphene.ResolveInfo):
        return [{
            "id": "op",
            "first_name": "my name is good",
            "email": "me@gmail.com"
        }]

    LabelQueryTypes  = type(type_name, (graphene.ObjectType, ), {
        type_name : graphene.Field(graphene.List(NodeType), args={
            "limit" : graphene.Argument(graphene.Int, description="limits the result count"),
            "offset" : graphene.Argument(graphene.Int, description="skips x results"),
            "dedup" : graphene.Argument(graphene.Boolean, description="dedups the result"),
            "order_by" : graphene.Argument(NodeOrderBy , description="order the result by"),
            "where": graphene.Argument(NodeWhereConditions)
        }),
        f"resolve_{type_name}" : resolve_query
    })

    return LabelQueryTypes

# LabelQueryTypes = create_label_query_type("Person")






