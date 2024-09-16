
# from invana_engine.graphql.generators.dataclasses import InvanaGraphSchema
from invana_engine import InvanaGraph
from invana_engine.backends.cypher.traversal import Neo4jTraversal
import graphene


class InvanaQueryBuilder:
    """This is the the common query language pattern in yaml/json formats 
    to be able to filter and traverse though the data in a graph. 
    
    """
    def __init__(self, graph:InvanaGraph, 
                #   graph_schema: InvanaGraphSchema
                  ) -> None:
        # self.graph_schema  = graph_schema # schema definitions of nodes and relationships
        self.graph = graph

    def build_query_from_graphql_info(self, info:graphene.ResolveInfo ):
        pass


    def build_query_from_traversal_config(self, traversal_config):

        
        return traversal_config
        
    

