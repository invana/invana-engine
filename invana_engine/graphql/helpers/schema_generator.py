# import graphene
# from .ariadne import AriadneGraphQLSchemaGenerator, AdriadneSchemUtils
# from ..generators.queries import QueryGenerators
# from ..queries.client import BasicInfoType
# from ..queries.hello import HelloType
# from ..queries.raw_query import ExecuteQueryType
# from ..subscriptions.execute_query import SubscriptionExample


# class SchemaGenerator:

#     """
#     example usage 

    
#     schema_str = \"""


#         type Movie {
#             title: String
#             actors: [Actor!]! @relationship(label: "ACTED_IN", direction: IN, properties: "ActedIn")
#         }

#         type Actor {
#             name: String
#             movies: [Movie!]! @relationship(label: "ACTED_IN", direction: OUT, properties: "ActedIn")
#         }

#         interface ActedIn @relationshipProperties {
#             roles: [String]
#         }

# \"""
#     schema_generator = SchemaGenerator()
    
    

#     """

#     def __init__(self, schema_str) -> None:
#         self.schema_str = schema_str
#         self.interim_schema = AriadneGraphQLSchemaGenerator().create_interim_schema(schema_str)
#         self.type_defs_dict = AdriadneSchemUtils().get_type_defs_dict(self.interim_schema)
    
#     def generate_query_types(self, *type_def_classes):
#         return type("Query", (
#             BasicInfoType, 
#             ExecuteQueryType,
#             *type_def_classes
#         ), {})
        
#     def generate_mutation_types(self,  *type_def_classes):
#         return type("Mutation", (
#             HelloType,
#             *type_def_classes
#         ), {})

#     def generate_subscription_types(self,  *type_def_classes):
#         return type("Subscription", ( 
#             SubscriptionExample,
#             *type_def_classes
#         ), {})
    
#     def get_schema(self, auto_camelcase=False):
#         query_classes = []
#         mutation_classes =[]
#         subscription_classes = []

#         for type_name, type_def_dict in self.type_defs_dict.items():
#             LabelQueryTypes = QueryGenerators(type_name, type_def_dict).generate()
#             query_classes.append(LabelQueryTypes)            

#         Query = self.generate_query_types(*query_classes)
#         Mutation = self.generate_mutation_types(*mutation_classes)
#         Subscription = self.generate_subscription_types(*subscription_classes)
#         return graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription,
#                                 auto_camelcase=auto_camelcase)
    