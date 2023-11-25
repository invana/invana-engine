from dataclasses import dataclass
import typing
from graphql import GraphQLObjectType
import graphene

class InvanaGQLDirections:
    OUT = "out"
    IN = "in"
    BOTH =  "both"    


# GraphDirections = "out" | "in" | "both"
@dataclass
class RelationshipPath:
    label: str
    source_node_label : str # lambda: NodeLabelType
    target_node_label : str # lambda: NodeLabelType


@dataclass(frozen=True)
class RelationshipField:
    field_name: str # field on which this directive is added 
    direction: InvanaGQLDirections
    other_node_label: str
    relationship_label: str
    directives: typing.Dict[str,   typing.Dict]

    def has_relationship_name(self, rel_name) -> str:
        return self.directives['relationship'].properties == rel_name
    
    def get_relationship_data(self) -> 'RelationshipField':
        return self.directives['relationship']
    
    @property
    def path(self) -> RelationshipPath:
        return RelationshipPath(
            label= self.relationship_label,
            source_node_label=None, 
            target_node_label=None
        )
        # path : RelationshipPath
    # relationship_label: str # relationship label
    # properties: str # relationship properties
    # node_label: str # return data Node

    # def __repr__(self) -> str:
    #     return f"<RelationshipDirective "

@dataclass
class PropertyField:
    field_name: str
    field_type_str: str
    field_type: typing.Any
    directives: typing.Dict[str,  typing.Dict]

    # def is_relationship_field(self) -> bool:
    #     if "relationship" in self.directives:
    #         return True
    #     return False

    # def is_data_field(self)-> bool:
    #     return not self.is_relationship_field()

# @dataclass
# class InvanaGQLRelationshipDefinition:
#     label: str
#     fields : typing.Dict[str, PropertyField]
#     def_string : str
#     schema: 'GraphSchema' # this is the entire schema data; just incase needed



@dataclass(frozen=False)
class RelationshipSchema:
    label: str
    data_fields: typing.Dict[str, PropertyField]
    def_string : str # gql definition strin
    type: GraphQLObjectType
    schema: 'GraphSchema' # this is the entire schema data; just incase needed

    def paths(self) -> typing.List[RelationshipPath]:
        return []

@dataclass(frozen=False)
class NodeSchema:
    label: str
    # label_type: str
    data_fields: typing.Dict[str, PropertyField]
    relationship_fields : typing.Dict[str, RelationshipField]
    def_string : str
    type: GraphQLObjectType
    schema: 'GraphSchema' # this is the entire schema data; just incase needed

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
        if direction.lower() in ["in", "out"]:
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
    nodes : typing.Dict[str, NodeSchema]
    relationships : typing.Dict[str, NodeSchema]
    schema_definition_str: str # graphql schema string representation
