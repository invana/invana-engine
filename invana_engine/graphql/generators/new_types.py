import typing
import graphene
from dataclasses import dataclass
from .gql_types import InvanaGQLSchema


@dataclass
class NodeLabelSchema:
    label: str
    properties: typing.Dict[str, typing.Union[graphene.ObjectType, graphene.List[graphene.ObjectType]]]

@dataclass
class RelLabelSchema:
    """
    label format: {self.inv.label}__{self.label}__{self.outv.label}
    """
    label: str
    properties: typing.Dict[str, typing.Union[graphene.ObjectType, graphene.List[graphene.ObjectType]]]
    inv: NodeLabelSchema
    outv: NodeLabelSchema

@dataclass
class NodeSchemaAggregate:
    label: str
    properties: typing.Dict[str, typing.Union[graphene.ObjectType, graphene.List[graphene.ObjectType]]]
    out_edges : typing.List[RelLabelSchema] # outgoing relationship schemas
    in_edges: typing.List[RelLabelSchema] # incoming relationship schemas
    both_edges : typing.List[RelLabelSchema] # both outgoing and incoming relationship schemas
    # indexes/contraints

@dataclass
class RelSchemaAggregate:
    """
    label format: self.label
    """
    label: str
    properties: typing.Dict[str, typing.Union[graphene.ObjectType, graphene.List[graphene.ObjectType]]]
    out_nodes : typing.List[NodeLabelSchema] # outgoing node schemas
    in_nodes : typing.List[NodeLabelSchema] # incoming node schemas
    both_nodes : typing.List[NodeLabelSchema] # both outgoing and incoming node schemas
    # indexes/contraints

class Schema:
    node_aggregates : typing.Dict[str, NodeSchemaAggregate]
    relationship_aggregates : typing.Dict[str, RelSchemaAggregate]
    gql_schema: InvanaGQLSchema
