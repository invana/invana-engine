import typing
import graphene
from .generators.resolvers import resolve_graph_schema
from .generators.dataclasses import InvanaGraphSchema
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
    label = graphene.String()
    # source_node = graphene.Field(lambda: NodeLabelSchema)
    # target_node = graphene.Field(lambda: NodeLabelSchema)
    source_node_label = graphene.String() 
    target_node_label = graphene.String()


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

class InvanaGraphSchema(graphene.ObjectType):
    nodes = graphene.Field(graphene.List(NodeLabelSchema))
    relationships = graphene.Field(graphene.List(RelationshipLabelSchema))

class GraphSchemeQuery(graphene.ObjectType):
    _schema = graphene.Field(InvanaGraphSchema)
    resolve__schema = resolve_graph_schema
