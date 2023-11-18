from dataclasses import dataclass
import typing
from graphql import GraphQLObjectType


class InvanaGQLDirections:
    OUT = "out"
    IN = "in"
    BOTH =  "both"    

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
    
    def get_relationship_data(self) -> InvanaGQLFieldRelationshipDirective:
        return self.directives['relationship']
    
    def is_data_field(self)-> bool:
        return not self.is_relationship_field()
    
@dataclass
class InvanaGQLLabelDefinition:
    label: str
    label_type: str
    fields: typing.Dict[str, InvanaGQLLabelFieldDefinition]
    def_string : str
    type: GraphQLObjectType

    def get_data_fields(self)-> typing.Dict[str, InvanaGQLLabelFieldDefinition]:
        return {field_name: field for field_name, field in self.fields.items() if field.is_data_field()}

    def get_relationship_fields(self)-> typing.Dict[str, InvanaGQLLabelFieldDefinition]:
        return {field_name: field for field_name, field in self.fields.items() if field.is_relationship_field()}
 
    def get_fields_grouped_by_relationship_label(self, direction: str="both") -> typing.Dict[str, InvanaGQLFieldRelationshipDirective]:
        """_summary_

        Args:
            direction (str, optional): _description_. Defaults to "both".

        Returns:
            {
                '_bothe__ACTED_IN': [InvanaGQLFieldRelati...'ActedIn'), InvanaGQLFieldRelati...'ActedIn')], 
                '_bothe__likes': [InvanaGQLFieldRelati...s='Liked')], 
                '_bothe': [InvanaGQLFieldRelati...'ActedIn'), InvanaGQLFieldRelati...s='Liked'), InvanaGQLFieldRelati...'ActedIn')]
            }
        """
        relationship_fields = self.get_relationship_fields()
        if direction in ["in", "out"]:
            field_relationships = [field.get_relationship_data() for _, field in relationship_fields.items() \
                    if field.get_relationship_data().direction == direction]
        else:
            field_relationships = [field.get_relationship_data() for _, field in relationship_fields.items()]

        fields_dict = {}
        # 1. grouped by relationship label "_oute__ACTED_IN"
        for field_relationship in field_relationships:
            key = f'_{direction}e__{field_relationship.relationship_label}'
            if fields_dict.get(key) and field_relationship not in fields_dict.get(key):
                    fields_dict[key].append(field_relationship)
            else:
                fields_dict[key] = [field_relationship]

        # 2. individual traversal "_oute__ACTED_IN__Movie" and "_oute__ACTED_IN__ShortFilm"
        if direction != "both":
            for relationship in field_relationships:
                # 2. inividual relationship label
                key = f"_{relationship.direction}e__{relationship.relationship_label}__{relationship.node_label}"
                fields_dict[key] = [relationship]
 
        # 3. generic in/out/both "_oute"
        all_types = [] 
        for field_name, field  in fields_dict.items():
            all_types.extend(field) 
        all_types=  list(set(all_types))
        if all_types.__len__() > 0:
            fields_dict[f"_{direction}e"] =all_types
 
        return fields_dict

    def get_related_fields(self):
        # seperate the in and out relationships
        related_fields = {}
        related_fields.update(self.get_fields_grouped_by_relationship_label(direction="both"))
        related_fields.update(self.get_fields_grouped_by_relationship_label(direction="in"))
        related_fields.update(self.get_fields_grouped_by_relationship_label(direction="out"))
        return related_fields
 

@dataclass
class InvanaGQLSchema:
    nodes : typing.Dict[str, InvanaGQLLabelDefinition]
    relationships : typing.Dict[str, InvanaGQLLabelDefinition]