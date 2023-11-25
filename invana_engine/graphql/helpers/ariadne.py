
from ariadne import make_executable_schema
from ariadne import SubscriptionType, make_executable_schema, MutationType, QueryType


class AriadneInterimSchemaGenerator:
    """
    Used to generate temporary graphql instance from user graphql definition
    """

 
    type_def_base = """

        # https://ariadnegraphql.org/docs/0.10.0/django-integration#date-and-datetime-scalars
        # https://www.apollographql.com/docs/apollo-server/v3/schema/creating-directives/
        scalar Date
        scalar DateTime


        enum RelationDirection{
            OUT
            IN
        }

        directive @relationship(label: String, direction: RelationDirection!, properties: String ) on FIELD_DEFINITION
        directive @relationshipProperties on INTERFACE | OBJECT
        """
    type_def_end = """

        type Query {
            hello: String
        }

        type Mutation {
            ok: String
        }
        
        type Subscription {
            counter: Int!
        }
"""

    def __init__(self) -> None:
        self.subscription = SubscriptionType()
        self.mutation = MutationType()
        self.query = QueryType()

    def create_interim_schema(self, type_def):
        # schema is created by adding dummy Query, Mutation , Subscription
        return self.create_schema(self.type_def_base + type_def + self.type_def_end)

    def create_schema(self, type_def, *type_defs):
        # full 
        return make_executable_schema(type_def, self.query, self.mutation, self.subscription, *type_defs)

