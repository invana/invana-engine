import graphene
from ..queries.client import BasicInfoType
from ..queries.hello import HelloType
from ..queries.raw_query import ExecuteQueryType
from ..subscriptions.execute_query import SubscriptionExample
from ariadne import make_executable_schema
from ariadne import SubscriptionType, make_executable_schema, MutationType, QueryType, ObjectType
import asyncio
from graphql import GraphQLObjectType , GraphQLField




class FinalGraphQLSchemaGenerator:

    def get_field_of_type(self, field):
        if hasattr(field, 'of_type'):
            return self.get_field_of_type(field.of_type)
        return field
    
    def get_directives_on_field(self, field):
        directives = field.ast_node.directives
        data = {}
        for directive in directives:
            _ = directive.name.value
            data[directive.name.value] = {}
            for argument in  directive.arguments:
                data[directive.name.value][argument.name.value] =  argument.value.value
            
        return data
    
    def generate_schema(self, interim_schema):
        nodes = []  
        relationships = []
        new_schema_str = ""
        for type_name, type_ in interim_schema.type_map.items():
            if isinstance(type_, GraphQLObjectType) and  type_.name not in  ["Query",
                            "Mutation", "Subscription"] and not type_.name.startswith("__")  :
                nodes.append(type_)
                body = type_.ast_node.loc.source.body
                # get node definition 
                def_string = body[type_.ast_node.loc.start: type_.ast_node.loc.end]            
                nodes.append(def_string)
                new_schema_str += "\n" + def_string
                # get if there are any relationshis in the fields
                for field_string, field  in type_.fields.items():
                    if field.ast_node.directives.__len__() > 0 :
                        field_type = self.get_field_of_type(field.type)
                        directives_dict = self.get_directives_on_field(field)
                        pass
        return new_schema_str



class AriadneGraphQLSchemaGenerator:

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
    type_def_end = """

        type Query {
            hello: String
        }

        type Mutation {
            ok: String
        }
        
        type Subscription {
            counter: Int!
        }
"""
    def __init__(self) -> None:
        self.subscription = SubscriptionType()
        self.mutation = MutationType()
        self.query = QueryType()


    def create_interim_schema(self, type_def):
        return self.type_def_base + type_def + self.type_def_end


    def get_schema(self, type_def, *type_defs):
        return make_executable_schema(type_def, self.query, self.mutation, self.subscription, *type_defs)



def generate_schema_dynamically():

    type_def = """

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

"""

    schema_generator = AriadneGraphQLSchemaGenerator()
    interim_schema_str = schema_generator.create_interim_schema(type_def)
    interim_schema = schema_generator.get_schema(interim_schema_str)


    final_schema_generator = FinalGraphQLSchemaGenerator()
    final_schema_str = final_schema_generator.generate_schema(interim_schema)

    return interim_schema
