import graphene
from invana_engine import InvanaGraph
from .dataclasses import InvanaGraphSchema
from graphql.language import  FieldNode
import typing
from invana_engine.query_builder.invana_ql import InvanaQueryBuilder


def generate_traversal_config(field_nodes: typing.List[FieldNode] ):
    data = {}
    for field in field_nodes:
        if field.selection_set:
            data[field.name.value] = generate_traversal_config(field.selection_set.selections)
        else:
            data[field.name.value] = True
    return data

def default_node_type_search_by_id_resolve_query(self, info: graphene.ResolveInfo, **kwargs):
    graph: InvanaGraph = info.context['request'].app.state.graph
    return []

def default_relationship_type_search_by_id_resolve_query(self, info: graphene.ResolveInfo, **kwargs):
    return []


def default_node_type_search_resolve_query(self, info: graphene.ResolveInfo, *args,  **kwargs):
    graph: InvanaGraph = info.context['request'].app.state.graph
    # graph_schema: InvanaGraphSchema = info.context['request'].app.state.graph_schema
    traversal_config = generate_traversal_config(info.field_nodes)
    graph_query = InvanaQueryBuilder(graph).build_query_from_traversal_config(traversal_config)

    # requested_fields_dict = [field.to_dict() for field in requested_fields]
    print("=====kwargs", kwargs)
    print("=====graph_query", graph_query)
    print("=====traversal_config", traversal_config)
    return []


def resolve_relationship_field_resolver(self, info: graphene.ResolveInfo, **kwargs):
    return []


def resolve_graph_schema(self, info:graphene.ResolveInfo, **kwargs):
    graph_schema = info.context['request'].app.state.graph_schema
    return graph_schema.to_json()
