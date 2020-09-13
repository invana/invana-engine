from graphene import Scalar, ObjectType, String


class GenericJSONField(Scalar):
    ''' convert the Json String into Json '''

    @staticmethod
    def serialize(dt):
        return dt

    @staticmethod
    def parse_literal(node):
        return node.value

    @staticmethod
    def parse_value(value):
        return value


class GraphElement(ObjectType):
    id = String()
    type = String()
    label = String()
    properties = GenericJSONField()
