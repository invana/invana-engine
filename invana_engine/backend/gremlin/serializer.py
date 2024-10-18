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
from invana_engine.types import RelationShip, Node, Path


class InvanaMapType(graphsonV3d0.MapType):

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
        _ = dict_data.copy()
        id = get_id(_[T.id])
        label = _[T.label]
        inv = _[Direction.IN]
        outv = _[Direction.OUT]
        del _[T.id]
        del _[T.label]
        del _[Direction.IN]
        del _[Direction.OUT]
        return RelationShip(
            id=id,
            label=label,
            outv=outv,
            inv=inv,
            properties=_)

    @classmethod
    def objectify(cls, l, reader):
        new_dict = super(InvanaMapType, cls).objectify(l, reader)
        if T.id in new_dict and Direction.IN not in new_dict:
            return cls.create_node_object(new_dict)
        if T.id in new_dict and Direction.IN in new_dict:
            return cls.create_relationship_object(new_dict)
        return new_dict


class InvanaVertexDeserializer(graphsonV3d0.VertexDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        return Node(
            id=reader.toObject(
                get_id(
                    d["id"])), label=d.get(
                "label", "vertex"))


class InvanaEdgeDeserializer(graphsonV3d0.EdgeDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        return RelationShip(
            id=reader.toObject(
                get_id(
                    d["id"])), label=d.get(
                "label", "edge"), inv=Node(
                    id=reader.toObject(
                        d["outV"]), label=d.get(
                            "outVLabel", "vertex")), outv=Node(
                                id=reader.toObject(
                                    d["inV"]), label=d.get(
                                        "inVLabel", "vertex")))


class InvanaPathDeserializer(graphsonV3d0.PathDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        return Path(
            reader.toObject(
                d["labels"]), reader.toObject(
                d["objects"]))


# class PropertyDeserializer(graphsonV3d0.PropertyDeserializer):
#
#     @classmethod
#     def objectify(cls, d, reader):
#         element = reader.toObject(d["element"]) if "element" in d else None
#         return Property(d["key"], reader.toObject(d["value"]), element)


INVANA_DESERIALIZER_MAP = {
    "g:Map": InvanaMapType,
    "g:Vertex": InvanaVertexDeserializer,
    "g:Edge": InvanaEdgeDeserializer,
    "g:Path": InvanaPathDeserializer,

    # "g:Property": InvanaEdgeDeserializer,
}
