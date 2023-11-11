import graphene
from .queries.client import BasicInfoType
from .queries.hello import HelloType
from .queries.querytypes import ExecuteQueryType
from .subscriptions.execute_query import SubscriptionExample
from ariadne import make_executable_schema
from ariadne import SubscriptionType, make_executable_schema, MutationType, QueryType
import asyncio


class GrapheneGraphQLSchemaGenerator:

    def generate_query_types(self):
        return type("Query", (
            BasicInfoType, 
            ExecuteQueryType
        ), {})
        
    def generate_mutation_types(self):
        return type("Mutation", (
            HelloType,
        ), {})

    def generate_subscription_types(self):
        return type("Subscription", ( 
            SubscriptionExample,
        ), {})
        
    def get_schema(self):
        Query = self.generate_query_types()
        Mutation = self.generate_mutation_types()
        Subscription = self.generate_subscription_types()
        return graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)


class AriadneGraphQLSchemaGenerator:

    def __init__(self) -> None:
        self.subscription = SubscriptionType()
        self.mutation = MutationType()
        self.query = QueryType()

    def get_schema(self, type_def):
        return make_executable_schema(type_def, self.query, self.mutation, self.subscription)


def example_schema_with_subscription():
    type_def = """
        type Query {
            _unused: Boolean
        }
        
        type Mutation {
            _unused: Boolean
        }

        type Subscription {
            counter: Int!
        }
    """
    schema_generator = AriadneGraphQLSchemaGenerator()
 
    @schema_generator.subscription.source("counter")
    async def counter_generator(obj, info):
        for i in range(50):
            await asyncio.sleep(1)
            yield i

    @schema_generator.subscription.field("counter")
    def counter_resolver(count, info):
        return count + 1
    
    return schema_generator.get_schema(type_def)




def example_schema():
    type_def = """
        interface Node {
            id: ID!
            label: String!
        }

        interface Relationship implements Node {
            id: ID!
            label: String!
            inv: ID!
            outv: ID!
        }

        type Person implements Node {
            id: ID!
            label: String!
            name: String
        }


        type Project implements Node {
            id: ID!
            label: String!
            name: String
        }
        
        type Query {
            person: Person
        }

        type Mutation {
            ok: String
        }
        
        type Subscription {
            counter: Int!
        }
    """

    schema_generator = AriadneGraphQLSchemaGenerator()
 
    @schema_generator.subscription.source("counter")
    async def counter_generator(obj, info):
        for i in range(50):
            await asyncio.sleep(1)
            yield i


    @schema_generator.subscription.field("counter")
    def counter_resolver(count, info):
        return count + 1
    
    return schema_generator.get_schema(type_def)
