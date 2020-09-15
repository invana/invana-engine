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


class GrapheneVertexType(ObjectType):
    id = String()
    type = String()
    label = String()
    properties = GenericJSONField()


class GrapheneEdgeType(ObjectType):
    id = String()
    type = String()
    label = String()
    properties = GenericJSONField()
    in_v = String()
    out_v = String()
    in_v_label = String()
    out_v_label = String()
