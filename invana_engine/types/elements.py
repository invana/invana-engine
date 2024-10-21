from dataclasses import dataclass
import typing as T


ElementIdType = T.Union[str, int]
PropertiesType = T.Dict[str, T.Any]
GenericData = T.Dict[str, T.Any]


@dataclass
class GenericData:
    data: dict

    def to_json(self):
        return self.data


@dataclass
class Property:
    id: T.Optional[ElementIdType]
    key: str
    value: any

    def __repr__(self) -> str:
        return f"vp[{self.key}={self.value}]"

@dataclass
class VertexProperty(Property):
    pass


@dataclass
class ElementBase:
    id: ElementIdType
    label: str
    properties: T.Optional[PropertiesType]

    def properties_to_json(self):
        properties = {}
        for property in self.properties:
            properties[property.key] = property.value
        return properties


@dataclass
class Node(ElementBase):
    type: str = "vertex"
    properties: T.List[VertexProperty]

    def __repr__(self):
        return f'<Node:{self.label} id="{self.id}" {self.properties}>'

    def __short_repr__(self):
        return f'<Node:{self.label}-{self.id}>'

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "properties": self.properties_to_json()}


@dataclass
class UnLabelledNode(Node):
    label: T.Optional[str]


@dataclass
class RelationShip(ElementBase):
    inv: T.Union[ElementIdType, Node, UnLabelledNode]  # to
    outv: T.Union[ElementIdType, Node, UnLabelledNode]  # from
    properties: T.Optional[T.List[Property]]
    type: str = "edge"

    def __repr__(self):
        return f'<RelationShip:{self.label}::{self.id} ' \
            f'({self.outv.__short_repr__()}) -> {self.label} -> ({self.inv.__short_repr__()})' \
            f' {self.properties}>'

    def to_json(self):
        base_data = {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "properties": self.properties_to_json()
        }
        base_data['inv'] = self.inv.to_json()
        base_data['outv'] = self.outv.to_json()
        return base_data


@dataclass
class UnLabelledRelationShip(RelationShip):
    label: T.Optional[str]
    inv: T.Optional[T.Union[ElementIdType, Node, UnLabelledNode]]  # to
    outv: T.Optional[T.Union[ElementIdType, Node, UnLabelledNode]]  # from
