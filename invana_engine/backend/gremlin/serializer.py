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
        properties = dict_data.copy()
        id = get_id(properties[T.id])
        label = properties[T.label]
        del properties[T.id]
        del properties[T.label]
        return Node(id=id, label=label, properties=properties)

    @staticmethod
    def create_relationship_object(dict_data):
        properties = dict_data.copy()
        id = get_id(properties[T.id])
        label = properties[T.label]
        inv = properties[Direction.IN]
        outv = properties[Direction.OUT]
        del properties[T.id]
        del properties[T.label]
        del properties[Direction.IN]
        del properties[Direction.OUT]
        return RelationShip(
            id=id,
            label=label,
            outv=outv,
            inv=inv,
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
        element = reader.to_object(d["element"]) if "element" in d else None
        return Property(id=get_id(reader.to_object(d["id"])), key=d["label"],
                         value=reader.to_object(d["value"]))


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
        return RelationShip(
                id=reader.to_object(get_id(d["id"])), 
                label=d.get("label", "edge"), 
                inv=Node(id=reader.to_object(d["outV"]), 
                        label=d.get("outVLabel", "vertex")), 
                outv=Node(id=reader.to_object(d["inV"]), 
                        label=d.get("inVLabel", "vertex")),
                properties=edge.properties

            )


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
