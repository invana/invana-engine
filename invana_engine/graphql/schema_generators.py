import graphene
from .queries.client import BasicInfoType
from .queries.hello import HelloType
from .queries.querytypes import ExecuteQueryType
from .subscriptions.execute_query import SubscriptionExample
from ariadne import make_executable_schema



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
