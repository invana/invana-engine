import graphene
from .queries.client import BasicInfoType
from .queries.hello import HelloType
from .queries.querytypes import ExecuteQueryType
from .subscriptions.execute_query import SubscriptionExample
from ariadne import make_executable_schema
from ariadne import SubscriptionType, make_executable_schema
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


    def get_schema(self, type_def, subscription):
        return make_executable_schema(type_def, subscription)


def example_schema_with_subscription():
    type_def = """
        type Query {
            _unused: Boolean
        }

        type Subscription {
            counter: Int!
        }
    """

    subscription = SubscriptionType()

    @subscription.source("counter")
    async def counter_generator(obj, info):
        for i in range(50):
            await asyncio.sleep(1)
            yield i


    @subscription.field("counter")
    def counter_resolver(count, info):
        return count + 1
    return type_def, subscription