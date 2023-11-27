from dataclasses import dataclass, asdict
import typing
from graphql import GraphQLObjectType


class RelationshipDirections:
    OUT = "OUT"
    IN = "IN"
    BOTH =  "BOTH"    


class FieldCardinality:
    SINGLE = "SINGLE"
    SET = "SET"
    LIST = "LIST"


class RelationshipMultiplicity:
    SIMPLE = "SIMPLE"
    MULTI = "MULTI"
    MANY2ONE = "MANY2ONE"
    ONE2MANY = "ONE2MANY"
    ONE2ONE = "ONE2ONE"


@dataclass
class RelationshipPath:
    label: str
    source_node_label : str # lambda: NodeLabelType
    target_node_label : str # lambda: NodeLabelType

    def to_json(self):
        return {k: str(v) for k, v in asdict(self).items()}

@dataclass(frozen=True)
class RelationshipField:
    field_name: str # field on which this directive is added 
    direction: RelationshipDirections
    other_node_label: str
    this_nodel_label: str
    relationship_label: str
    directives: typing.Dict[str,   typing.Dict]

    # def has_relationship_name(self, rel_name) -> str:
    #     return self.directives['relationship'].properties == rel_name
    
    def get_relationship_data(self) -> 'RelationshipField':
        return self.directives['relationship']
    
    @property
    def path(self) -> RelationshipPath:
        kwargs = {
            "label": self.relationship_label
        }
        if self.direction == RelationshipDirections.IN:
            kwargs['source_node_label'] = self.other_node_label
            kwargs['target_node_label'] = self.this_nodel_label
        elif self.direction == RelationshipDirections.OUT:
            kwargs['source_node_label'] =  self.this_nodel_label
            kwargs['target_node_label'] =self.other_node_label 
        else:
            raise Exception("direction cannot be out")
        return RelationshipPath(**kwargs)
 
    def to_json(self):
        return {k: str(v) for k, v in asdict(self).items()}

@dataclass
class PropertyField:
    field_name: str
    field_type_str: str
    field_type: typing.Any
    directives: typing.Dict[str,  typing.Dict]
    cardinality: FieldCardinality = FieldCardinality.SINGLE

    def to_json(self):
        return {
            "name": self.field_name,
            "data_type": self.field_type_str,
            "cardinality": self.cardinality
        }
        # return {k: str(v) for k, v in asdict(self).items()}


@dataclass(frozen=False)
class RelationshipSchema:
    label: str
    data_fields: typing.Dict[str, PropertyField]
    def_string : str # gql definition strin
    type: GraphQLObjectType
    schema: 'GraphSchema' # this is the entire schema data; just incase needed
    multiplicity: str = RelationshipMultiplicity.MULTI

    @property
    def paths(self) -> typing.List[RelationshipPath]:
        paths = []
        for node in self.schema.nodes:
            paths.extend(node.relationship_paths)
        return paths

    def to_json(self):
        return {
            "label": self.label,
            "properties": [ field.to_json() for k, field in self.data_fields.items()],
            "multiplicity": self.multiplicity,
            "relationship_paths": self.paths
        }
        # return {k: str(v) for k, v in asdict(self).items()}

@dataclass(frozen=False)
class NodeSchema:
    label: str
    data_fields: typing.Dict[str, PropertyField]
    relationship_fields : typing.Dict[str, RelationshipField]
    def_string : str
    type: GraphQLObjectType
    schema: 'GraphSchema' # this is the entire schema data; just incase needed

    def to_json(self, ):
        return {
            "label": self.label,
            "properties": [ field.to_json() for k, field in self.data_fields.items()],
            "property_keys": self.property_keys,
            "relationship_paths": self.relationship_paths
        }
    
    @property
    def relationship_paths(self):
        return [field.path.to_json() for field_name, field in self.relationship_fields.items()]
    
    @property
    def property_keys(self):
        return [ field.field_name for field_name, field in self.data_fields.items()]

    @property
    def all_fields(self):
        return {**self.data_fields, **self.relationship_fields}

    def get_relationship_fields_by_direction(self, direction: str):
        """_summary_

        Args:
            direction (str): _description_
        """
        if direction  in ["IN", "OUT"]:
            return  [field for _, field in self.relationship_fields.items() \
                    if field.direction.lower() == direction]
        return [field for _, field in self.relationship_fields.items()]

    def directed_relationship_to_node(self, direction):
        """
        Create relationships grouped by relationship label. ex: "out__related_to__Node

        Args:
            direction (_type_): out, in, both
        """
        # if direction == "both":
        #     raise Exception("directed_relationship_to_node direction cannot be 'both', because"
        #                     "each relationship will have a direction to a Node")
        field_relationships = self.get_relationship_fields_by_direction(direction)
        fields_dict = {}
        for relationship_field in field_relationships:
            # 2. inividual relationship label
            key = f"{relationship_field.direction.lower()}e__{relationship_field.relationship_label}__{relationship_field.other_node_label}"
            fields_dict[key] = relationship_field
        return fields_dict
         
    def directed_relationships_grouped_by_edge_label(self, direction):
        """
        Create relationships grouped by relationship label. ex: "_oute__ACTED_IN"

        Args:
            direction (_type_): in, out, both
        """
        field_relationships = self.get_relationship_fields_by_direction(direction)
        fields_dict = {}
        for field_relationship in field_relationships:
            key = f'{direction}e__{field_relationship.relationship_label}'
            if fields_dict.get(key) and field_relationship not in fields_dict.get(key):
                fields_dict[key].append(field_relationship)
            else:
                fields_dict[key] = [field_relationship]
        return fields_dict
    
    def generic_directed_relationships(self, direction):
        """
        Create relationships grouped by relationship label. ex: "_oute


        Args:
            direction (_type_): out, in, both
        """
        fields_dict = self.directed_relationships_grouped_by_edge_label(direction)
        node_types = [] 
        for field_name, field  in fields_dict.items():
            node_types.extend(field) 

        # create this if there are any node related 
        if node_types.__len__() > 0:
            fields_dict[f"{direction}e"] = node_types
        return fields_dict
         

@dataclass
class GraphSchema:
    nodes : typing.List[NodeSchema]
    relationships : typing.List[NodeSchema]
    schema_definition_str: str # graphql schema string representation

    def to_json(self):
        return {
            "nodes": [node.to_json() for node in self.nodes],
            "relationships": [relationship.to_json() for relationship in self.relationships],
            "schema_definition_str": self.schema_definition_str
        }
        # return {k: str(v) for k, v in asdict(self).items()}

    def get_node_schema(self, label) -> NodeSchema:
        return list(filter(lambda node : node.label == label, self.nodes))[0]
    
    def get_relationship_schema(self, label) -> RelationshipSchema:
        return list(filter(lambda relationship : relationship.label == label, self.relationships))[0]