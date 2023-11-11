import graphene


"""

"""
OrderByEnum = type("OrderByEnum", (graphene.Enum, ), {"asc": "asc", "desc": "desc"})


"""
all the types above are generic reusable
"""
class PersonType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()


class PersonAggregateType(graphene.ObjectType):
    aggregate_by = graphene.String()

    def resolve_aggregate_by(self, *_):
        pass


PersonOrderBy = type("PersonOrderBy", (graphene.InputObjectType, ), 
                    {"id": OrderByEnum(), "name": OrderByEnum()} ) 

# PersonWhereConditions = type("PersonWhereConditions", (graphene.InputObjectType, ){

# })

class LabelQueryTypes(graphene.ObjectType):

    person = graphene.Field(graphene.List(PersonType), args={
        "_limit" : graphene.Argument(graphene.Int, description="limits the result count"),
        "_offset" : graphene.Argument(graphene.Int, description="skips x results"),
        "_dedup" : graphene.Argument(graphene.Boolean, description="dedups the result"),
        "_order_by" : graphene.Argument(PersonOrderBy , description="order the result by"),
        "_where": graphene.Argument(graphene.String)
    })
    # person_aggregate = graphene.Field(PersonAggregateType)
    # person_by_id= graphene.Field()

    def resolve_person(self, info: graphene.ResolveInfo,
                       
                       ):
        pass

    # def resolve_person_aggregate(self, info: graphene.ResolveInfo, ,b):
    #     pass




