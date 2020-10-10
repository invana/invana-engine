from graphene import Scalar, ObjectType, String, ID, DateTime
import datetime

class AnyField(Scalar):


    @staticmethod
    def serialize(dt):
        if isinstance(dt, dict):
            transformed_data = {}
            for key, v in dt.items():
                if isinstance(v, datetime.datetime):
                    transformed_data[key] =  v.isoformat()
                else:
                    transformed_data[key] = v
            return transformed_data
        else:
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
