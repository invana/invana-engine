import graphene
from .schema_generators.queries.client import BasicInfoType
from .schema_generators.queries.run_query import RunQueryObjectType


class SchemaGenerator:

    def __init__(self, schema_str: str) -> None:
        self.schema_str = schema_str

    def generate_query_types(self, *type_def_classes):
        return type("Query", (
            BasicInfoType,
            RunQueryObjectType,
            *type_def_classes
        ), {})

    # def generate_mutation_types(self, *type_def_classes):
    #     return type("Mutation", (
    #         # HelloType,
    #         *type_def_classes
    #     ), {})

    def get_schema(self, auto_camelcase=False):
        query_classes = []

        Query = self.generate_query_types(*query_classes)
        return graphene.Schema(query=Query,
                               auto_camelcase=auto_camelcase)
