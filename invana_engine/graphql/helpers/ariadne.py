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
        # schema is created by adding dummy Query, Mutation , Subscription
        return self.create_schema(self.type_def_base + type_def + self.type_def_end)


    def create_schema(self, type_def, *type_defs):
        # full 
        return make_executable_schema(type_def, self.query, self.mutation, self.subscription, *type_defs)



class AdriadneSchemUtils():

    # def __init__(self, interim_schema) -> None:
    #     self.interim_schema = interim_schema

    def get_type_of_field(self, field):
        if hasattr(field, 'of_type'):
            return self.get_type_of_field(field.of_type)
        return field
    
    def get_directives_on_field(self, field):
        directives = field.ast_node.directives
        data = {}
        for directive in directives:
            _ = directive.name.value
            data[directive.name.value] = {}
            for argument in  directive.arguments:
                data[directive.name.value][argument.name.value] =  argument.value.value
            data[directive.name.value]['node_label'] = self.get_type_of_field(field.type).name
            data[directive.name.value]['relation_label'] = data[directive.name.value]['label']
            del data[directive.name.value]['label']
        return data
    
    def get_field_defintion_str(self, type_):
        body = type_.ast_node.loc.source.body
        return body[type_.ast_node.loc.start: type_.ast_node.loc.end]  
    
    def get_type_defs(self, type_: GraphQLObjectType):
        type_def_dict = {}
        type_def_dict['def_string'] = self.get_field_defintion_str(type_)
        type_def_dict['type'] = type_
        type_def_dict['fields'] = {}
        
        # get if there are any relationshis in the fields
        for field_string, field  in type_.fields.items():
            field_type = self.get_type_of_field(field.type)
            type_def_dict['fields'][field_string] = {
                'field_type_str' : field_type.name,
                'field_type' : field_type,
                'directives' : {}
            }
            # this will get the relationships 
            if field.ast_node.directives.__len__() > 0 :
                directives_dict = self.get_directives_on_field(field)
                type_def_dict['fields'][field_string]['directives'] = directives_dict
        return type_def_dict
    
    def get_type_defs_dict(self,interim_schema):
        type_defs_dict = {} 
        for type_name, type_ in interim_schema.type_map.items():
            if isinstance(type_, GraphQLObjectType) and  type_.name not in  ["Query",
                            "Mutation", "Subscription"] and not type_.name.startswith("__")  :                
                type_defs_dict[type_name] = self.get_type_defs(type_)
        return type_defs_dict
    