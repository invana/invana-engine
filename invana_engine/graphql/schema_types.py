import typing
import graphene
from .generators.resolvers import resolve_graph_schema
from .generators.gql_types import GraphSchema
from importlib import import_module

PropertyCardinalityEnum = type( "PropertyCardinalityEnum",  (graphene.Enum,), {
    "SINGLE" : "SINGLE",
    "LIST" : "LIST",
    "SET": "SET"
})


RelationshipDirectionEnum = type('RelationshipDirection',(graphene.Enum, ), {
    "OUT": "OUT",
    "IN": "IN"
} )

RelationshipMultiplicityEnum = type('RelationshipMultiplicity',(graphene.Enum, ), {
    "MULTI": "MULTI",
    "MULTI": "MULTI",
    "MANY2ONE": "MANY2ONE",
    "ONE2MANY": "ONE2MANY",
    "ONE2ONE": "ONE2ONE"
} )


class DataPropertyField(graphene.ObjectType):
    name =  graphene.String()
    data_type = graphene.String() # int, dict, list, nullable or  etc 
    cardinality =  PropertyCardinalityEnum()
    default_value =  graphene.String()
    description = graphene.String()

class RelationshipPath(graphene.ObjectType):
    relationship_label = graphene.String()
    source_node = graphene.Field(lambda: NodeLabelSchema)
    # target_node_label = graphene.Field(getattr(import_module(__name__), 'NodeLabelSchema'))
    target_node = graphene.Field(lambda: NodeLabelSchema)

class NodeLabelSchema(graphene.ObjectType):
    label =  graphene.Field(graphene.String)
    properties = graphene.Field(graphene.List(DataPropertyField))
    property_keys = graphene.List(graphene.String)
    relationship_paths = graphene.Field(graphene.List(RelationshipPath)) # all unique relationships per source and target label
 
class RelationshipLabelSchema(graphene.ObjectType):
    label = graphene.String()
    properties = graphene.List(DataPropertyField)
    multiplicity = RelationshipMultiplicityEnum()
    relationship_paths = graphene.List(RelationshipPath)

class GraphSchema(graphene.ObjectType):
    nodes = graphene.Field(graphene.List(NodeLabelSchema))
    relationships = graphene.Field(graphene.List(RelationshipLabelSchema))

class GraphSchemeQuery(graphene.ObjectType):
    _schema = graphene.Field(GraphSchema)

    resolve__schema = resolve_graph_schema

# @dataclass
# class RelLabelSchema:
#     """
#     label format: {self.inv.label}__{self.label}__{self.outv.label}
#     """
#     label: str # relationship label, ex: Actor__acted_in__Movie
#     properties: typing.Dict[str, typing.Union[graphene.ObjectType, graphene.List[graphene.ObjectType]]]
#     incoming_node: NodeLabelSchema # target/to node  
#     outgoing_node: NodeLabelSchema # source/from node 
#     # field_on_node: str # this is the field on type definition in which relationship is defined. ex: movies

# @dataclass
# class NodeSchemaAggregate:
#     label: str
#     properties: typing.Dict[str, typing.Union[graphene.ObjectType, graphene.List[graphene.ObjectType]]]
#     out_edges : typing.List[RelLabelSchema] # outgoing relationship schemas
#     in_edges: typing.List[RelLabelSchema] # incoming relationship schemas
#     both_edges : typing.List[RelLabelSchema] # both outgoing and incoming relationship schemas
#     # indexes/contraints

# @dataclass
# class RelationshipLabelSchema:
#     """
#     label format: self.label
#     """
#     label: graphene
#     properties: typing.Dict[str, typing.Union[graphene.ObjectType, graphene.List[graphene.ObjectType]]]
#     out_nodes : typing.List[NodeLabelSchema] # outgoing node schemas
#     in_nodes : typing.List[NodeLabelSchema] # incoming node schemas
#     both_nodes : typing.List[NodeLabelSchema] # both outgoing and incoming node schemas
#     # indexes/contraints



# class Schema:
#     node_aggregates : typing.Dict[str, NodeSchemaAggregate]
#     relationship_aggregates : typing.Dict[str, RelSchemaAggregate]
#     gql_schema: GraphSchema
