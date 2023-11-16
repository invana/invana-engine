from dataclasses import dataclass
import typing
from graphql import GraphQLObjectType


@dataclass
class InvanaGQLFieldRelationshipDirective:
    node_label: str
    relation_label: str
    direction: str
    properties: str

@dataclass
class InvanaGQLLabelDefinitionField:
    field_type_str: str
    field_type: typing.Any
    directives: typing.Dict[str, typing.Union[InvanaGQLFieldRelationshipDirective, typing.Any]]

    def is_relationship_field(self) -> bool:
        if "relationship" in self.directives:
            return True
        return False
    
    def get_relationship_data(self) -> bool:
        return self.directives['relationship']
    
    def is_data_field(self)-> bool:
        return not self.is_relationship_field()
    
@dataclass
class InvanaGQLLabelDefinition:
    label: str
    label_type: str
    def_string : str
    type: GraphQLObjectType
    fields: typing.Dict[str, InvanaGQLLabelDefinitionField]

    def get_data_fields(self)-> typing.Dict[str, InvanaGQLLabelDefinitionField]:
        return {field_name: field for field_name, field in self.fields.items() if field.is_data_field()}

    def get_relationship_fields(self)-> typing.Dict[str, InvanaGQLLabelDefinitionField]:
        return {field_name: field for field_name, field in self.fields.items() if field.is_relationship_field()}

@dataclass
class InvanaGQLSchema:
    nodes : typing.Dict[str, InvanaGQLLabelDefinition]
    relationships : typing.Dict[str, InvanaGQLLabelDefinition]