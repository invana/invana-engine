from dataclasses import dataclass
import typing
from graphql import GraphQLObjectType


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
