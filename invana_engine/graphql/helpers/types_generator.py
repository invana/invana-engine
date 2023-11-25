from graphql import GraphQLObjectType , GraphQLField, GraphQLInterfaceType
import typing
from dataclasses import dataclass
from graphql.type.schema import GraphQLSchema
from ..generators.dataclasses import RelationshipField, NodeSchema,\
      PropertyField, GraphSchema, RelationshipSchema


class GraphSchemaTypesGeneratorUtil():
    """
    take interim schema as input and outputs  `..generators.gql_types.GraphSchema`
    """

    def get_type_of_field(self, field):
        if hasattr(field, 'of_type'):
            return self.get_type_of_field(field.of_type)
        return field
    
    def get_directives_on_field(self, field_name:str, field: GraphQLField) -> \
                typing.Dict[str, typing.Union[RelationshipField, typing.Any]]:
        directives = field.ast_node.directives
        data = {}
        for directive in directives:
            datum = {}
            for argument in  directive.arguments:
                datum[ argument.name.value] =  argument.value.value
            data[directive.name.value] = datum
        return data

    def get_directives_on_type(self, type_: GraphQLObjectType):
        directives = type_.ast_node.directives
        data = {}
        for directive in directives: 
            # if hasattr(directive, 'value'):
            data[directive.name.value] = True #TODO - fix this later for directives with values
        return data
    
    def get_type_defintion_str(self, type_: GraphQLObjectType):
        body = type_.ast_node.loc.source.body
        return body[type_.ast_node.loc.start: type_.ast_node.loc.end]  
    
    def get_element_type(self, type_: GraphQLObjectType):
        directives =  self.get_directives_on_type(type_)
        if "relationshipProperties" in directives:
            return "relationship"
        return "node"
    
    def get_type_defs(self, type_: GraphQLObjectType) -> typing.Union[NodeSchema, RelationshipSchema]:
        
        label_type = self.get_element_type(type_)
        type_def_dict = {}
        type_def_dict['def_string'] = self.get_type_defintion_str(type_)
        type_def_dict['type'] = type_
        type_def_dict['label'] = type_.name
        type_def_dict['data_fields'] = {}
        type_def_dict['relationship_fields'] = {}
        type_def_dict['schema'] = None

        # get if there are any relationshis in the fields
        for field_name, field  in type_.fields.items():
            # this will get the relationships 
            field_type = self.get_type_of_field(field.type)
            field_data = {
                "field_name": field_name,
                "directives": {}
            }
            if field.ast_node.directives.__len__() > 0 :
                field_data['directives'] = self.get_directives_on_field(field_name, field)

            if "relationship" in field_data['directives']:
                # this is for relationship field 
                relationship_data = field_data['directives']['relationship']
                field_data.update({
                    "direction": relationship_data['direction'],
                    "relationship_label": relationship_data['label'],
                    "other_node_label": field_type.name,
                    "this_nodel_label": type_.name
                })
                type_def_dict['relationship_fields'][field_name] = RelationshipField(**field_data)
            else:
                # this is for data field
                field_data.update({
                    'field_type_str' : field_type.name,
                    'field_type' : field_type,
                    'directives' : {}
                })
                type_def_dict['data_fields'][field_name] = PropertyField(**field_data)

        if label_type == "relationship":
            del type_def_dict['relationship_fields']
        return NodeSchema(**type_def_dict) if label_type == "node" else RelationshipSchema(**type_def_dict)

    def create_schema_instance(self,schema_str:str, interim_schema: GraphQLSchema) -> GraphSchema:
        schema_items_dict = {} 
        for type_name, type_ in interim_schema.type_map.items():
            if (isinstance(type_, GraphQLObjectType) or isinstance(type_, GraphQLInterfaceType)) \
                    and  type_.name not in  ["Query", "Mutation", "Subscription"] \
                    and not type_.name.startswith("__")  :                
                schema_items_dict[type_name] = self.get_type_defs(type_)

        # create chema instance 
        schema :GraphSchema  = {"nodes": [],"relationships": [], "schema_definition_str": schema_str}
        for label, label_def in schema_items_dict.items():
            if isinstance(label_def, NodeSchema):
                schema['nodes'].append(label_def)
            elif isinstance(label_def, RelationshipSchema):
                schema['relationships'].append(label_def)
        schema_instance =  GraphSchema(**schema)

        # attache schema to all the labelDefinitions
        for label_def in schema_instance.relationships:
            setattr(label_def, 'schema', schema_instance)
        for label_def in schema_instance.nodes:
            setattr(label_def, 'schema', schema_instance)

        return schema_instance
