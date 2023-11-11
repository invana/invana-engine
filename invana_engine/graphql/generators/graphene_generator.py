import graphene
from ..queries.client import BasicInfoType
from ..queries.hello import HelloType
from ..queries.raw_query import ExecuteQueryType
from ..queries.node_label_filters import LabelQueryTypes
from ..subscriptions.execute_query import SubscriptionExample
from ariadne import make_executable_schema
from ariadne import SubscriptionType, make_executable_schema, MutationType, QueryType, ObjectType
import asyncio
from ariadne import SubscriptionType
from datetime import datetime





class GrapheneGraphQLSchemaGenerator:

    def generate_query_types(self):
        return type("Query", (
            BasicInfoType, 
            ExecuteQueryType,
            LabelQueryTypes
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

