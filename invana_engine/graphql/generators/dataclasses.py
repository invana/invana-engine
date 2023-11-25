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

    @property
    def paths(self) -> typing.List[RelationshipPath]:
        return [] # TODO - 

    def to_json(self):
        return {k: str(v) for k, v in asdict(self).items()}

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
        # for path in paths:
        #     path['source_node'] = self.schema.get_node_schema(path['source_node_label']).to_json(),
        #     path['target_node'] = self.schema.get_node_schema(path['target_node_label']).to_json(),
        # return paths
    
    @property
    def property_keys(self):
        return [ field.field_name for field_name, field in self.data_fields.items()]

    @property
    def all_fields(self):
        return {**self.data_fields, **self.relationship_fields}

    def get_inv_and_outv_fields(self):
        if self.label_type == "node":
            raise Exception("only label_type='relationship' will have inv and outv fields ")
        
    def get_relationship_fields(self)-> typing.Dict[str, RelationshipField]:
        """all the fields that has relationship directives

        Returns:
            typing.Dict[str, PropertyField]: _description_
        """
        return self.relationship_fields
 
    def get_relationships_by_label(self, rel_label) -> bool:
        """
        Checks if the current node label has relationship to 

        Args:
            rel_label (_type_): _description_

        Returns:
            bool: _description_
        """
        related_fields = {}
        for field_name, field in self.relationship_fields.items():
            # if field.has_relationship_name(rel_label):
            related_fields[field_name] = field
        return related_fields
            
    def get_related_nodes_by_relationship(self, rel_label: str):
        """
        Returns all the NodeLabelDefinition that has this the relationship rel_label 

        Args:
            rel_label (str): _description_
        """
        related_node_fields = {}
        for node_label , node in self.schema.nodes.items():
            related_node_fields.update(node.get_relationships_by_label(rel_label)) 
        return related_node_fields

    def get_relationship_fields_by_direction(self, direction: str):
        """_summary_

        Args:
            direction (str): _description_
        """
        relationship_fields = self.get_relationship_fields()
        if direction  in ["IN", "OUT"]:
            return  [field for _, field in relationship_fields.items() \
                    if field.direction.lower() == direction]
        return [field for _, field in relationship_fields.items()]

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
            key = f"_{relationship_field.direction.lower()}e__{relationship_field.relationship_label}__{relationship_field.other_node_label}"
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
            key = f'_{direction}e__{field_relationship.relationship_label}'
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
        all_types = [] 
        for field_name, field  in fields_dict.items():
            all_types.extend(field) 

        if all_types.__len__() > 0:
            fields_dict[f"_{direction}e"] = all_types
        return fields_dict
         

@dataclass
class GraphSchema:
    nodes : typing.List[NodeSchema]
    relationships : typing.List[NodeSchema]
    schema_definition_str: str # graphql schema string representation

    def to_json(self):
        return {
            "nodes": [node.to_json() for node in self.nodes],
            "relationships": [],
            "schema_definition_str": self.schema_definition_str
        }
        # return {k: str(v) for k, v in asdict(self).items()}

    def get_node_schema(self, label) -> NodeSchema:
        return list(filter(lambda node : node.label == label, self.nodes))[0]
    
    def get_relationship_schema(self, label) -> RelationshipSchema:
        return list(filter(lambda relationship : relationship.label == label, self.relationships))[0]