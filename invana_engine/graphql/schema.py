import graphene
from .types.client import ClientInfoType
from .types.hello import HelloType



class GraphQLSchemaGenerator:


    def generate_query_types(self):
        return type("Query", (
            ClientInfoType, 
            HelloType
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
