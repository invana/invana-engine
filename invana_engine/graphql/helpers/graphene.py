import graphene
from ..queries.client import BasicInfoType
from ..queries.hello import HelloType
from ..queries.raw_query import ExecuteQueryType
from ..subscriptions.execute_query import SubscriptionExample


class GrapheneGraphQLSchemaGenerator:

    def generate_query_types(self, *type_def_classes):
        return type("Query", (
            BasicInfoType, 
            ExecuteQueryType,
            *type_def_classes
        ), {})
        
    def generate_mutation_types(self):
        return type("Mutation", (
            HelloType,
        ), {})

    def generate_subscription_types(self):
        return type("Subscription", ( 
            SubscriptionExample,
        ), {})
        
    def get_schema(self, auto_camelcase=False):
        Query = self.generate_query_types()
        Mutation = self.generate_mutation_types()
        Subscription = self.generate_subscription_types()

        return graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription,
                                auto_camelcase=auto_camelcase)