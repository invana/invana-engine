from graphene import Scalar, ObjectType, String, ID


class AnyField(Scalar):

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
    id = AnyField()
    type = String()
    label = String()
    properties = AnyField()


class GrapheneEdgeType(ObjectType):
    id = AnyField()
    type = String()
    label = String()
    properties = AnyField()
    in_v = String()
    out_v = String()
    in_v_label = String()
    out_v_label = String()
