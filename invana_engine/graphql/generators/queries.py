import graphene
from .dataclasses import  NodeSchema, RelationshipSchema, GraphSchema
# from .exceptions import UnSupportedFieldDirective
from .utils import NodeGenerator, RelationshipGenerator
import typing
from .resolvers import default_node_type_search_resolve_query, resolve_relationship_field_resolver,\
    default_node_type_search_by_id_resolve_query, default_relationship_type_search_by_id_resolve_query


class QueryGenerators(NodeGenerator, RelationshipGenerator):
 
    def __init__(self, graph_schema: GraphSchema) -> None:
        self.graph_schema = graph_schema


    def create_node_type_search_field_with_resolver(self, 
                        type_def: NodeSchema,
                        extra_args=None) -> typing.Dict[str, typing.Union[graphene.Field, typing.Callable]]:
        fields = {}
        fields[type_def.label] =  self.create_node_type_search_field(type_def, extra_args=extra_args)
        fields[f"resolve_{type_def.label}"]  = default_node_type_search_resolve_query
        return fields
        
    def create_relationship_type_search_field_with_resolver(self, 
                        type_def: RelationshipSchema,
                        extra_args=None) -> typing.Dict[str, typing.Union[graphene.Field, typing.Callable]]:
        fields = {}
        fields[type_def.label] =  self.create_relationship_type_search_field(type_def, extra_args=extra_args)
        fields[f"resolve_{type_def.label}"]  = resolve_relationship_field_resolver
        return fields
        
    def create_node_type_search_by_id_field_with_resolver(self, 
                        type_def: NodeSchema,
                        extra_args=None) -> typing.Dict[str, typing.Union[graphene.Field, typing.Callable]]:
        extra_args = {} if extra_args is None else extra_args
        fields = {}
        fields[f'{type_def.label}_by_id'] = self.create_node_type_search_by_id_field(type_def, extra_args=extra_args)
        fields[f"resolve_{type_def.label}_by_id"]  = default_node_type_search_by_id_resolve_query
        return fields
    
    def create_relationship_type_search_by_id_field_with_resolver(self, 
                        type_def: NodeSchema,
                        extra_args=None) -> typing.Dict[str, typing.Union[graphene.Field, typing.Callable]]:
        extra_args = {} if extra_args is None else extra_args
        fields = {}
        fields[f'{type_def.label}_by_id'] = self.create_relationship_type_search_by_id_field(type_def, extra_args=extra_args)
        fields[f"resolve_{type_def.label}_by_id"]  = default_relationship_type_search_by_id_resolve_query
        return fields
    
    def create_entire_graph_search_with_resolver(self):
        node_fields = {}
        # add over all arguments 
        # add fields
        # where filters
        #        on all fields 
        #        on label_type, labels
        node_fields["_graph"] =  graphene.Field(graphene.List(graphene.String)) # TODO - this is mocked
        node_fields[f"resolve__graph"]  = default_node_type_search_resolve_query
        return node_fields

    def generate(self):
        #  type_def: NodeSchema,
        query_classes = []

        for type_def in self.graph_schema.nodes:
            # label search
            node_fields = self.create_node_type_search_field_with_resolver( type_def)
            query_classes.append(type(type_def.label, (graphene.ObjectType, ), node_fields))         
            # label search by id 
            node_fields = self.create_node_type_search_by_id_field_with_resolver( type_def)
            query_classes.append(type(f'{type_def.label}_by_id', (graphene.ObjectType, ), node_fields))         
 
        for type_def in self.graph_schema.relationships:
            # label search 
            node_fields = self.create_relationship_type_search_field_with_resolver(type_def)
            query_classes.append(type(type_def.label, (graphene.ObjectType, ), node_fields))         
            # label search by id
            node_fields = self.create_relationship_type_search_by_id_field_with_resolver( type_def)
            query_classes.append(type(f'{type_def.label}_by_id', (graphene.ObjectType, ), node_fields))         
 
        node_fields = self.create_entire_graph_search_with_resolver()
        query_classes.append(type("_graph", (graphene.ObjectType, ), node_fields))         

        return query_classes
