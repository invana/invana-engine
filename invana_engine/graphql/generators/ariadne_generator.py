import graphene
from ..queries.client import BasicInfoType
from ..queries.hello import HelloType
from ..queries.raw_query import ExecuteQueryType
from ..subscriptions.execute_query import SubscriptionExample
from ariadne import make_executable_schema
from ariadne import SubscriptionType, make_executable_schema, MutationType, QueryType, ObjectType
import asyncio
from graphql import GraphQLObjectType , GraphQLField
import pathlib
import os 


class FinalGraphQLSchemaGenerator:


    def __init__(self, interim_schema) -> None:
        self.interim_schema = interim_schema
        self.final_schema_str = open(os.path.join(
                pathlib.Path(__file__).parent.resolve(), "graphql_base.graphql", ), "r").read()


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
    

    # def create_field(self, field):
    #     pass


    def get_field_defintion(self, type_):
        body = type_.ast_node.loc.source.body
        return body[type_.ast_node.loc.start: type_.ast_node.loc.end]  
    
    def get_type_defs_dict(self, ):
        type_defs_dict = {} 
        for type_name, type_ in self.interim_schema.type_map.items():
            if isinstance(type_, GraphQLObjectType) and  type_.name not in  ["Query",
                            "Mutation", "Subscription"] and not type_.name.startswith("__")  :
                
                type_defs_dict[type_name] = {}
                type_defs_dict[type_name]['def_string'] = self.get_field_defintion(type_)
                type_defs_dict[type_name]['type'] = type_
                type_defs_dict[type_name]['fields'] = {}
                

                # get if there are any relationshis in the fields
                for field_string, field  in type_.fields.items():
                    field_type = self.get_field_of_type(field.type)
                    type_defs_dict[type_name]['fields'][field_string] = {
                        'field_type_str' : field_type.name,
                        'field_type' : field_type
                    }
                    if field.ast_node.directives.__len__() > 0 :
                        directives_dict = self.get_directives_on_field(field)
                        type_defs_dict[type_name]['fields'][field_string]['directives'] = directives_dict

        return type_defs_dict
    

    # def create_new_type(self, type_name, type_data):


        # node_def = """
        # \"""select properties of Node "{type_name}"\"""
        # enum {type_name}_select_property {
        #     {properties}
        # }
 
        # \"""
        # fetch data from the table: "Project"
        # \"""
        # {type_name}(
        #     \"""distinct select on properties\"""
        #     distinct_on: [{type_name}_select_property!]

        #     \"""limit the number of rows returned\"""
        #     limit: Int

        #     \"""skip the first n rows. Use only with order_by\"""
        #     offset: Int

        #     \"""sort the rows by one or more columns\"""
        #     order_by: [Project_order_by!]

        #     \"""filter the rows returned\"""
        #     where: Project_bool_exp
        # ): [{type_name}!]!        
        
        # """.format(type_name=type_name, properties="\n".join(type_data['fields'].keys()))
        
        # return node_def
    
    def generate_schema(self):
        type_defs_dict = self.get_type_defs_dict()
        
        for type_name, type_data in type_defs_dict.items():
            # self.final_schema_str += self.create_new_type(type_name, type_data)
            pass
                        

        return self.final_schema_str



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


    final_schema_generator = FinalGraphQLSchemaGenerator(interim_schema)
    final_schema_str = final_schema_generator.generate_schema()
    return interim_schema

    # final_schema = schema_generator.get_schema(final_schema_str)

    # return final_schema
