import graphene
from ..queries.client import BasicInfoType
from ..queries.hello import HelloType
from ..queries.raw_query import ExecuteQueryType
from ..subscriptions.execute_query import SubscriptionExample
from ariadne import make_executable_schema
from ariadne import SubscriptionType, make_executable_schema, MutationType, QueryType, ObjectType
import asyncio

 
class AriadneGraphQLSchemaGenerator:

    def __init__(self) -> None:
        self.subscription = SubscriptionType()
        self.mutation = MutationType()
        self.query = QueryType()

    def get_schema(self, type_def, *type_defs):
        return make_executable_schema(type_def, self.query, self.mutation, self.subscription, *type_defs)



def generate_schema_dynamically():
    type_def_base = """

        # https://ariadnegraphql.org/docs/0.10.0/django-integration#date-and-datetime-scalars
        scalar Date
        scalar DateTime


        enum RelationDirection{
            OUT
            IN
        }

        directive @relationship(label: String, direction: RelationDirection!) on FIELD_DEFINITION
"""
    type_def = """

        type Person {
            id: ID!
            label: String!
            name: String
        }

        type Project {
            id: ID!
            label: String!
            name: String
            owner: [Person!]! @relationship(label: "has_project", direction: IN)
        }

"""
    type_def_end = """

        type Query {
            person: Person
            project: Project
        }

        type Mutation {
            ok: String
        }
        
        type Subscription {
            counter: Int!
        }
"""
    schema_generator = AriadneGraphQLSchemaGenerator()
 
    _ = schema_generator.get_schema(type_def_base+ type_def + type_def_end)
    return _
