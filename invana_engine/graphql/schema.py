import graphene
from .types.client import BasicInfoType
from .types.hello import HelloType
from .types.querytypes import ExecuteQueryType



class GraphQLSchemaGenerator:


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
            HelloType,
        ), {})
        
   

    def get_schema(self):
        Query = self.generate_query_types()
        Mutation = self.generate_mutation_types()
        Subscription = self.generate_subscription_types()
        return graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
