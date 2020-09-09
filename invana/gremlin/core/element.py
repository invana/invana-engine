"""


"""


class CreateElement:
    pass


class SerializedElement:
    id = None
    label = None
    type = None
    properties = {}

    @staticmethod
    def serialized_data(data, serializer=None):
        return serializer.serialize_data(data)

    def __init__(self, data, serializer=None):
        self.data = data
        serialized_data = self.serialized_data(data, serializer=serializer)
        self.assign_id_label_properties(serialized_data['id'], serialized_data['label'],
                                        serialized_data['properties'])

    def assign_id_label_properties(self, id, label, properties):
        self.id = id
        self.label = label
        self.properties = properties

    def __dict__(self):
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type,
            "properties": self.properties
        }

    def __repr__(self):
        return "<{type} label={label} id={id}> ".format(type=self.type.capitalize(),
                                                        id=self.id, label=self.label)

    def get_property(self, key):
        return self.properties.get(key)


class VertexElement(SerializedElement):
    type = "vertex"


class EdgeElement(SerializedElement):
    type = "edge"
