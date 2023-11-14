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
import typing
from dataclasses import dataclass
from graphql.type.schema import GraphQLSchema

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


@dataclass
class InvanaGQLFieldRelationshipDirective:
    node_label: str
    relation_label: str
    direction: str

@dataclass
class InvanaGQLLabelDefinitionField:
    field_type_str: str
    field_type: typing.Any
    directives: typing.Dict[str, typing.Union[InvanaGQLFieldRelationshipDirective, typing.Any]]

@dataclass
class InvanaGQLLabelDefinition:
    label: str
    def_string : str
    type: GraphQLObjectType
    fields: typing.Dict[str, InvanaGQLLabelDefinitionField]


class AdriadneSchemUtils():

    # def __init__(self, interim_schema) -> None:
    #     self.interim_schema = interim_schema


    def get_type_of_field(self, field):
        if hasattr(field, 'of_type'):
            return self.get_type_of_field(field.of_type)
        return field
    
    def get_directives_on_field(self, field) -> typing.Dict[str, typing.Union[InvanaGQLFieldRelationshipDirective, typing.Any]]:
        directives = field.ast_node.directives
        data = {}
        for directive in directives:
            datum = {}
            for argument in  directive.arguments:
                datum[argument.name.value] =  argument.value.value
            datum['node_label'] = self.get_type_of_field(field.type).name
            datum['relation_label'] = datum['label']
            del datum['label']
            data[directive.name.value] = InvanaGQLFieldRelationshipDirective(**datum)
        return data
    
    def get_field_definition(self, field):
        field_type = self.get_type_of_field(field.type)
        field_data = {
            'field_type_str' : field_type.name,
            'field_type' : field_type,
            'directives' : {}
        }
        # this will get the relationships 
        if field.ast_node.directives.__len__() > 0 :
            field_data['directives'] = self.get_directives_on_field(field)
        return InvanaGQLLabelDefinitionField(**field_data)
    
    def get_type_defintion_str(self, type_):
        body = type_.ast_node.loc.source.body
        return body[type_.ast_node.loc.start: type_.ast_node.loc.end]  
    
    def get_type_defs(self, type_: GraphQLObjectType) -> InvanaGQLLabelDefinition:
        type_def_dict = {}
        type_def_dict['def_string'] = self.get_type_defintion_str(type_)
        type_def_dict['type'] = type_
        type_def_dict['label'] = type_.name
        type_def_dict['fields'] = {}

        # get if there are any relationshis in the fields
        for field_name, field  in type_.fields.items():
            type_def_dict['fields'][field_name] = self.get_field_definition(field)
        return InvanaGQLLabelDefinition(**type_def_dict)
    
    def get_type_defs_dict(self,interim_schema: GraphQLSchema) -> typing.Dict[str, InvanaGQLLabelDefinition]:
        type_defs_dict = {} 
        for type_name, type_ in interim_schema.type_map.items():
            if isinstance(type_, GraphQLObjectType) and  type_.name not in  ["Query",
                            "Mutation", "Subscription"] and not type_.name.startswith("__")  :                
                type_defs_dict[type_name] = self.get_type_defs(type_)
        return type_defs_dict
    
