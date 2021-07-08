"""


"""


#  Copyright 2020 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

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
        self.assign_data(serialized_data)

    def assign_data(self, serialized_data):
        raise NotImplementedError()

    def assign_id_label_properties(self, _id, label, properties):
        self.id = _id
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
        return "<{type} label={label} id={id}> ".format(type=self.type,
                                                        id=self.id, label=self.label)

    def get_property(self, key):
        return self.properties.get(key)


class VertexElement(SerializedElement):
    type = "g:Vertex"

    def assign_data(self, serialized_data):
        self.assign_id_label_properties(serialized_data['id'], serialized_data['label'],
                                        serialized_data.get('properties', {}))


class EdgeElement(SerializedElement):
    type = "g:Edge"
    in_v = None
    in_v_label = None
    out_v = None
    out_v_label = None

    def assign_data(self, serialized_data):
        self.assign_id_label_properties(serialized_data['id'], serialized_data['label'],
                                        serialized_data.get('properties', {}),
                                        )
        self.in_v = serialized_data['inV']
        self.in_v_label = serialized_data['inVLabel']
        self.out_v = serialized_data['outV']
        self.out_v_label = serialized_data['outVLabel']

    def __dict__(self):
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type,
            "properties": self.properties,
            "in_v": self.in_v,
            "out_v": self.out_v,
            'in_v_label': self.in_v_label,
            'out_v_label': self.out_v_label
        }
