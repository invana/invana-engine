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
    key: str
    value: any
    id: T.Optional[ElementIdType] = None

    def __repr__(self) -> str:
        return f"P[{self.key}={self.value}]"


@dataclass
class VertexProperty(Property):

    def __repr__(self) -> str:
        return f"VP[{self.key}={self.value}]"


@dataclass
class ElementBase:
    id: ElementIdType
    label: str
    properties: T.Optional[PropertiesType]

    def properties_to_json(self):
        properties = {}
        if self.properties:
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
    inV: T.Union[ElementIdType, Node, UnLabelledNode]  # to
    outV: T.Union[ElementIdType, Node, UnLabelledNode]  # from
    properties: T.Optional[T.List[Property]]
    type: str = "edge"

    def __repr__(self):
        return f'<Link:{self.label}::{self.id} ' \
            f'({self.outV.__short_repr__()}) -> {self.label} -> ({self.inV.__short_repr__()})' \
            f' {self.properties}>'

    def to_json(self):
        base_data = {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "properties": self.properties_to_json()
        }
        base_data['inV'] = self.inV.to_json()
        base_data['outV'] = self.outV.to_json()
        return base_data


@dataclass
class UnLabelledRelationShip(RelationShip):
    label: T.Optional[str]
    inV: T.Optional[T.Union[ElementIdType, Node, UnLabelledNode]]  # to
    outV: T.Optional[T.Union[ElementIdType, Node, UnLabelledNode]]  # from
