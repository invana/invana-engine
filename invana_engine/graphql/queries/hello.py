import graphene


class HelloType(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="World"))
