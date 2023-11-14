from dataclasses import dataclass
from .types import ElementIdType , PropertiesType
import typing

@dataclass
class GenericData:
    data: dict
    
    def to_json(self):
        return self.data

@dataclass
class ElementBase:
    id: ElementIdType
    label: str
    properties: typing.Optional[PropertiesType]


@dataclass
class Node(ElementBase):
    type: str = "vertex"

    def __repr__(self):
        return f'<Node:{self.label} id="{self.id}" {self.properties}>'

    def __short_repr__(self):
        return f'<Node:{self.label}-{self.id}>'

    def to_json(self):
        return {"id": self.id, "type": self.type, "label": self.label, "properties": self.properties}


@dataclass
class UnLabelledNode(Node):
    label: typing.Optional[str]


@dataclass
class RelationShip(ElementBase):
    inv: typing.Union[ElementIdType, Node, UnLabelledNode]  # to
    outv: typing.Union[ElementIdType, Node, UnLabelledNode] # from
    type: str = "edge"

    def __repr__(self):
        return f'<RelationShip:{self.label}::{self.id} ' \
                f'({self.outv.__short_repr__()}) -> {self.label} -> ({self.inv.__short_repr__()})' \
                f' {self.properties}>'

    def to_json(self):
        base_data = {"id": self.id, "type": self.type, "label": self.label, "properties": self.properties}
        base_data['inv'] = self.inv.to_json()
        base_data['outv'] = self.outv.to_json()
        return base_data

@dataclass
class UnLabelledRelationShip(RelationShip):
    label: typing.Optional[str]
    inv: typing.Optional[typing.Union[ElementIdType, Node, UnLabelledNode]]  # to
    outv: typing.Optional[typing.Union[ElementIdType, Node, UnLabelledNode]] # from
