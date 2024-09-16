import graphene
from ..helpers.ariadne import AriadneInterimSchemaGenerator
from ..helpers.types_generator import GraphSchemaTypesGeneratorUtil
from .queries import QueryGenerators
from ..queries.client import BasicInfoType
from ..queries.hello import HelloType
from ..queries.raw_query import ExecuteQueryType
from ..subscriptions.execute_query import SubscriptionExample
from ..schema_types import GraphSchemeQuery


class SchemaGenerator:

    """
    example usage 

    
    schema_str = \"""


        type Person {
            id: ID!
            label: String!
            name: String
            projects: [Project!]! @relationship(label: "authored_project", direction: OUT)

        }

        type Project {
            id: ID!
            label: String!
            name: String
        }


\"""
    schema_generator = SchemaGenerator()
    
    

    """

    def __init__(self, schema_str: str) -> None:
        self.schema_str = schema_str
        self.graph_schema = self.generate_graph_schema()

    def generate_graph_schema(self):
        
        interim_schema = AriadneInterimSchemaGenerator().create_interim_schema(self.schema_str)
        return  GraphSchemaTypesGeneratorUtil().create_schema_instance(self.schema_str, interim_schema)
        
    def generate_query_types(self, *type_def_classes):
        return type("Query", (
            BasicInfoType, 
            ExecuteQueryType,
            *type_def_classes
        ), {})
        
    def generate_mutation_types(self,  *type_def_classes):
        return type("Mutation", (
            HelloType,
            *type_def_classes
        ), {})

    def generate_subscription_types(self,  *type_def_classes):
        return type("Subscription", ( 
            SubscriptionExample,
            *type_def_classes
        ), {})
    
    def get_schema(self, auto_camelcase=False):
        query_classes = []
        mutation_classes =[]
        subscription_classes = []

        query_classes = QueryGenerators(self.graph_schema).generate()
        query_classes.append(GraphSchemeQuery) # adding schema

        Query = self.generate_query_types(*query_classes)
        Mutation = self.generate_mutation_types(*mutation_classes)
        Subscription = self.generate_subscription_types(*subscription_classes)
        return graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription,
                                auto_camelcase=auto_camelcase)
    