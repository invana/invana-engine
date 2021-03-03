from graphene import Scalar, ObjectType, String, ID, DateTime, List, Boolean
import datetime


class AnyField(Scalar):

    @staticmethod
    def serialize(dt):
        if isinstance(dt, dict):
            transformed_data = {}
            for key, v in dt.items():
                if isinstance(v, datetime.datetime):
                    transformed_data[key] = v.isoformat()
                else:
                    transformed_data[key] = v
            return transformed_data
        elif isinstance(dt, datetime.datetime):
            return dt.isoformat()
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


class GrapheneEdgeType(GrapheneVertexType):
    in_v = AnyField()
    out_v = AnyField()
    in_v_label = String()
    out_v_label = String()


class GrapheneVertexOrEdgeType(GrapheneEdgeType):
    pass


class ElementSchemaType(ObjectType):
    label = String()
    propertyKeys = AnyField()


class StatusType(ObjectType):
    status = Boolean()
    message = String()
