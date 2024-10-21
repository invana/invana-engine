#    Copyright 2021 Invana
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#     http:www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
from gremlin_python.structure.io import graphsonV3d0
from gremlin_python.process.traversal import T, Direction
from .utils import get_id
from invana_engine.types import RelationShip, Node, \
    Property, VertexProperty


class MapType(graphsonV3d0.MapType):

    @staticmethod
    def create_node_object(dict_data):
        data = dict_data.copy()
        id = get_id(data[T.id])
        label = data[T.label]
        del data[T.id]
        del data[T.label]
        properties = []
        for key, value, in data.items():
            properties.append(VertexProperty(key=key, value=value))
        return Node(id=id, label=label, properties=properties)

    @staticmethod
    def create_relationship_object(dict_data):
        data = dict_data.copy()
        id = get_id(data[T.id])
        label = data[T.label]
        inV = data[Direction.IN]
        outV = data[Direction.OUT]
        del data[T.id]
        del data[T.label]
        del data[Direction.IN]
        del data[Direction.OUT]

        properties = []
        for key, value, in data.items():
            properties.append(Property(key=key, value=value))
        return RelationShip(
            id=id,
            label=label,
            outV=outV,
            inV=inV,
            properties=properties)

    @classmethod
    def objectify(cls, l, reader):
        new_dict = super(MapType, cls).objectify(l, reader)
        if T.id in new_dict and Direction.IN not in new_dict:
            return cls.create_node_object(new_dict)
        if T.id in new_dict and Direction.IN in new_dict:
            return cls.create_relationship_object(new_dict)
        return new_dict


class VertexPropertyDeserializer(graphsonV3d0.VertexPropertyDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        # element = reader.to_object(d["element"]) if "element" in d else None
        return VertexProperty(id=get_id(reader.to_object(d["id"])), key=d["label"],
                               value=reader.to_object(d["value"]))


class PropertyDeserializer(graphsonV3d0.PropertyDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        property = super(PropertyDeserializer, cls).objectify(d, reader)
        return Property(key=property.key, value=property.value)


class VertexDeserializer(graphsonV3d0.VertexDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        node = super(VertexDeserializer, cls).objectify(d, reader)
        return Node(
                id=node.id, 
                label=node.label,
                properties=node.properties
            )


class EdgeDeserializer(graphsonV3d0.EdgeDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        edge = super(EdgeDeserializer, cls).objectify(d, reader)

        # for property in edge.properties:
        #     print(property)
        _ = RelationShip(
                id=get_id(reader.to_object(d["id"])), 
                label=edge.label, 
                inV=Node(id=edge.inV.id, label=edge.inV.label, properties=edge.inV.properties), 
                outV=Node(id=edge.outV.id, label=edge.outV.label, properties=edge.outV.properties), 
                properties=edge.properties

            )
        return _


# class InvanaPathDeserializer(graphsonV3d0.PathDeserializer):

#     @classmethod
#     def objectify(cls, d, reader):
#         return Path(reader.to_object(d["labels"]), 
#                     reader.to_object(d["objects"])
#                 )



INVANA_DESERIALIZER_MAP = {
    "g:Map": MapType,
    "g:Vertex": VertexDeserializer,
    "g:Edge": EdgeDeserializer,
    "g:VertexProperty": VertexPropertyDeserializer,
    "g:Property": PropertyDeserializer
    # "g:Path": InvanaPathDeserializer
}
