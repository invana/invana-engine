import graphene


def default_node_type_resolve_query(self, info: graphene.ResolveInfo, **kwargs):
    return []


def resolve_relationship_field_resolver(self, info: graphene.ResolveInfo, **kwargs):
    return []
