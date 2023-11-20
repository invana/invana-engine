from dataclasses import dataclass
import typing
from graphql import GraphQLObjectType
import graphene

class InvanaGQLDirections:
    OUT = "out"
    IN = "in"
    BOTH =  "both"    


# GraphDirections = "out" | "in" | "both"

@dataclass(frozen=True)
class InvanaGQLFieldRelationshipDirective:
    node_label: str # return data Node
    field_name: str # field on which this directive is added 
    relationship_label: str # relationship label
    direction: InvanaGQLDirections
    properties: str # relationship properties

    # def __repr__(self) -> str:
    #     return f"<RelationshipDirective "

@dataclass
class InvanaGQLLabelFieldDefinition:
    field_type_str: str
    field_type: typing.Any
    directives: typing.Dict[str, typing.Union[InvanaGQLFieldRelationshipDirective, typing.Any]]

    def is_relationship_field(self) -> bool:
        if "relationship" in self.directives:
            return True
        return False
    
    def has_relationship_name(self, rel_name) -> str:
        return self.directives['relationship'].properties == rel_name
    
    def get_relationship_data(self) -> InvanaGQLFieldRelationshipDirective:
        return self.directives['relationship']
    
    def is_data_field(self)-> bool:
        return not self.is_relationship_field()
    

@dataclass(frozen=False)
class InvanaGQLLabelDefinition:
    label: str
    label_type: str
    fields: typing.Dict[str, InvanaGQLLabelFieldDefinition]
    def_string : str
    type: GraphQLObjectType
    schema: 'InvanaGQLSchema'

    def get_data_fields(self)-> typing.Dict[str, InvanaGQLLabelFieldDefinition]:
        return {field_name: field for field_name, field in self.fields.items() if field.is_data_field()}
    
    def get_inv_and_outv_fields(self):
        if self.label_type == "node":
            raise Exception("only label_type='relationship' will have inv and outv fields ")
        

    def get_relationship_fields(self)-> typing.Dict[str, InvanaGQLLabelFieldDefinition]:
        """all the fields that has relationship directives

        Returns:
            typing.Dict[str, InvanaGQLLabelFieldDefinition]: _description_
        """

        if self.label_type == "node":
            return {field_name: field for field_name, field in self.fields.items() if field.is_relationship_field()}
        return self.get_relationship_fields_reciprocal()

    def get_relationship_fields_reciprocal(self):
        """
        This is used by relationship label_type to get the reciprocal relationships
        """

        related_node_labels = self.get_related_nodes_by_relationship(self.label)
        for field_name, field in related_node_labels.items():
            # TODO - fix the directions and the field names 
            pass
            # for directive in directives:
            #     datum = {}
            #     datum['field_name'] = field_name
            #     for argument in  directive.arguments:
            #         # key =f"relationship_{argument.name.value}" if  argument.name.value  == "properties" else  argument.name.value
            #         datum[ argument.name.value] =  argument.value.value
            #     datum['node_label'] = self.get_type_of_field(field.type).name
            #     datum['relationship_label'] = datum['label']
            #     del datum['label']
            #     if "direction" in datum:
            #         datum['direction'] = datum['direction'].lower()
            #     data[directive.name.value] = InvanaGQLFieldRelationshipDirective(**datum)
            # field_data = {
            #     'field_type_str' : field_type.name,
            #     'field_type' : field_type,
            #     'directives' : {}
            # }
            # # this will get the relationships 
            # if field.ast_node.directives.__len__() > 0 :
            #     field_data['directives'] = self.get_directives_on_field(field_name, field)
            # return InvanaGQLLabelFieldDefinition(**field_data)
        return related_node_labels

    def get_relationships_by_label(self, rel_label) -> bool:
        """
        Checks if the current node label has relationship to 

        Args:
            rel_label (_type_): _description_

        Returns:
            bool: _description_
        """
        related_fields = {}
        for field_name, field in self.fields.items():
            if field.is_relationship_field() and field.has_relationship_name(rel_label):
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

        # if self.label_type == "node":
        relationship_fields = self.get_relationship_fields()
        # else:
        #     relationship_fields = self.get_relationship_fields_reciprocal()
        #     print("===")

        if direction in ["in", "out"]:
            return  [field.get_relationship_data() for _, field in relationship_fields.items() \
                    if field.get_relationship_data().direction == direction]
        return [field.get_relationship_data() for _, field in relationship_fields.items()]

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
        for relationship in field_relationships:
            # 2. inividual relationship label
            key = f"_{relationship.direction}e__{relationship.relationship_label}__{relationship.node_label}"
            fields_dict[key] = [relationship]
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
        all_types=  list(set(all_types))
        if all_types.__len__() > 0:
            fields_dict[f"_{direction}e"] =all_types
        return fields_dict
         

@dataclass
class InvanaGQLSchema:
    nodes : typing.Dict[str, InvanaGQLLabelDefinition]
    relationships : typing.Dict[str, InvanaGQLLabelDefinition]
    schema_definition_str: str # graphql schema string representation