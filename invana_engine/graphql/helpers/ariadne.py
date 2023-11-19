
from ariadne import make_executable_schema
from ariadne import SubscriptionType, make_executable_schema, MutationType, QueryType
from graphql import GraphQLObjectType , GraphQLField, GraphQLInterfaceType
import typing
from dataclasses import dataclass
from graphql.type.schema import GraphQLSchema
from ..generators.types import InvanaGQLFieldRelationshipDirective, InvanaGQLLabelDefinition,\
      InvanaGQLDataFieldDefinition, InvanaGQLSchema

class AriadneGraphQLSchemaGenerator:

 
    type_def_base = """

        # https://ariadnegraphql.org/docs/0.10.0/django-integration#date-and-datetime-scalars
        # https://www.apollographql.com/docs/apollo-server/v3/schema/creating-directives/
        scalar Date
        scalar DateTime


        enum RelationDirection{
            OUT
            IN
        }

        directive @relationship(label: String, direction: RelationDirection!, properties: String ) on FIELD_DEFINITION
        directive @relationshipProperties on INTERFACE | OBJECT
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
    

    def get_field_definition(self,field_name: str,  field: GraphQLField) -> InvanaGQLDataFieldDefinition:
        field_type = self.get_type_of_field(field.type)
        field_data = {
            'field_type_str' : field_type.name,
            'field_type' : field_type,
            'directives' : {}
        }
        # this will get the relationships 
        if field.ast_node.directives.__len__() > 0 :
            field_data['directives'] = self.get_directives_on_field(field_name, field)
        return InvanaGQLDataFieldDefinition(**field_data)

    def get_type_defintion_str(self, type_: GraphQLObjectType):
        body = type_.ast_node.loc.source.body
        return body[type_.ast_node.loc.start: type_.ast_node.loc.end]  
    
    def get_directives_on_field(self, field_name:str, field: GraphQLField) -> \
                typing.Dict[str, typing.Union[InvanaGQLFieldRelationshipDirective, typing.Any]]:
        directives = field.ast_node.directives
        data = {}

        for directive in directives:
            datum = {}
            datum['field_name'] = field_name
            for argument in  directive.arguments:
                # key =f"relationship_{argument.name.value}" if  argument.name.value  == "properties" else  argument.name.value
                datum[ argument.name.value] =  argument.value.value
            datum['node_label'] = self.get_type_of_field(field.type).name
            datum['relationship_label'] = datum['label']
            del datum['label']
            if "direction" in datum:
                datum['direction'] = datum['direction'].lower()
            data[directive.name.value] = InvanaGQLFieldRelationshipDirective(**datum)
        return data
    
    def get_directives_on_type(self, type_: GraphQLObjectType):
        directives = type_.ast_node.directives
        data = {}
        for directive in directives: 
            # if hasattr(directive, 'value'):
            data[directive.name.value] = True #TODO - fix this later for directives with values
        return data
    
    def get_element_type(self, type_: GraphQLObjectType):
        directives =  self.get_directives_on_type(type_)
        if "relationshipProperties" in directives:
            return "relationship"
        return "node"

    def get_type_defs(self, type_: GraphQLObjectType) -> InvanaGQLLabelDefinition:
        type_def_dict = {}
        type_def_dict['def_string'] = self.get_type_defintion_str(type_)
        type_def_dict['type'] = type_
        type_def_dict['label_type'] = self.get_element_type(type_)
        type_def_dict['label'] = type_.name
        type_def_dict['fields'] = {}
        type_def_dict['schema'] = None

        # get if there are any relationshis in the fields
        for field_name, field  in type_.fields.items():
            type_def_dict['fields'][field_name] = self.get_field_definition(field_name, field)
        return InvanaGQLLabelDefinition(**type_def_dict)

    def create_invana_schema(self,interim_schema: GraphQLSchema) -> InvanaGQLSchema:
        schema_items_dict = {} 
        for type_name, type_ in interim_schema.type_map.items():
            if (isinstance(type_, GraphQLObjectType) or isinstance(type_, GraphQLInterfaceType)) \
                    and  type_.name not in  ["Query", "Mutation", "Subscription"] \
                    and not type_.name.startswith("__")  :                
                schema_items_dict[type_name] = self.get_type_defs(type_)

        # create chema instance 
        schema :InvanaGQLSchema  = {"nodes": {},"relationships": {}}
        for label, label_def in schema_items_dict.items():
            if label_def.label_type == "relationship":
                schema['relationships'][label] = label_def
            else:
                schema['nodes'][label] = label_def
        schema_instance =  InvanaGQLSchema(**schema)

        # attache schema to all the labelDefinitions
        for label, label_def in schema_instance.relationships.items():
            setattr(label_def, 'schema', schema_instance)
        for label, label_def in schema_instance.nodes.items():
            setattr(label_def, 'schema', schema_instance)

        return schema_instance
