from .base import CRUDOperationsBase
import logging

logger = logging.getLogger(__name__)


class SchemaReadOperations(CRUDOperationsBase):

    def get_graph_schema(self):
        # TODO - can add more information from the print schema data like indexes etc to current output
        result = self.gremlin_client.query("mgmt = graph.openManagement(); mgmt.printSchema()")
        return self.process_graph_schema_string(result[0])

    def get_all_vertices_schema(self):
        # TODO - validate performance
        schema = self.get_graph_schema()
        schema_dict = {}
        for label in schema['vertex_labels']:
            schema_dict[label] = self.get_vertex_schema(label)
        return schema_dict

    def get_all_edges_schema(self):
        """

        :return:
        """
        # TODO - validate performance
        schema = self.get_graph_schema()
        schema_dict = {}
        for label in schema['edge_labels']:
            schema_dict[label] = self.get_edge_schema(label)
        return schema_dict

    def get_vertex_schema(self, label):
        return self.gremlin_client.query(
            "g.V().hasLabel('{label}').propertyMap().select(Column.keys).next();".format(label=label),
            serialize_elements=False
        ) or []

    def get_edge_schema(self, label):
        return self.gremlin_client.query(
            "g.E().hasLabel('{label}').propertyMap().select(Column.keys).next();".format(label=label),
            serialize_elements=False
        ) or []


class SchemaCreateUpdateOperations(CRUDOperationsBase):
    default_data_type = "String"
    default_cardinality_type = "SINGLE"
    allowed_data_types = [
        "String", "Character", "Boolean", "Byte", "Short", "Integer", "Long",
        "Float", "Double", "Date", "Geoshape", "UUID"
    ]
    allowed_cardinality_types = [
        "SINGLE", "LIST", "SET"
    ]

    def validate_data_type(self, data_type, property_label):
        if data_type not in self.allowed_data_types:
            raise Exception("only data types: {}  are allowed, "
                            "but received '{}' type for property {}".format(
                self.allowed_data_types, data_type, property_label))

    def validate_cardinality_type(self, cardinality_type, property_label):
        if cardinality_type not in self.allowed_cardinality_types:
            raise Exception("only cardinality types: {}  are allowed, "
                            "but received '{}' type for property {}".format(
                self.allowed_cardinality_types, cardinality_type, property_label))

    def create_schema_string_of_properties_schema(self, **properties_schema):
        """
        Refer https://docs.janusgraph.org/basics/schema/#property-key-data-type

        :param properties_schema: properties . example **{"name": {"data_type": "Long", "cardinality": "SINGLE"}}
        :return:
        """
        query_string = ""
        for property_label, property_schema in properties_schema.items():
            data_type = property_schema.get("data_type", self.default_data_type).capitalize()
            cardinality_type = property_schema.get("cardinality", self.default_cardinality_type).upper()

            self.validate_data_type(data_type, property_label)
            self.validate_data_type(data_type, property_label)
            # TODO - refactor janusgraph specific path for cardinality `org.janusgraph.core.`
            query_string += """
{property_label} = mgmt.makePropertyKey('{property_label}')
                            .dataType({data_type}.class)
                            .cardinality(org.janusgraph.core.Cardinality.{cardinality_type})
                            .make()""".format(property_label=property_label,
                                              cardinality_type=cardinality_type,
                                              data_type=data_type)
            # query_string += "{property_label} = mgmt.makePropertyKey('{property_label}')" \
            #                 ".dataType({data_type}.class)" \
            #                 ".cardinality(Cardinality.{cardinality_type})" \
            #                 ".make()\n".format(property_label=property_label,
            #                                    cardinality_type=cardinality_type,
            #                                    data_type=data_type)

        return query_string

    def create_schema(self, element_type, label, **properties_schema):
        query_string = """        
        mgmt = graph.openManagement()
        {label} = mgmt.make{element_type}Label('{label}').make()
                """.format(label=label, element_type=element_type.capitalize())
        query_string += self.create_schema_string_of_properties_schema(**properties_schema)
        query_string += "\nmgmt.addProperties({label},{properties})\n".format(
            label=label, properties=",".join(list(properties_schema.keys())))
        query_string += "mgmt.commit()"
        _ = self.gremlin_client.query(query_string, serialize_elements=False)
        return _

    def create_edge_label_with_schema(self, label, **properties_schema):
        """
        USAGE:
        create_edge_label_with_schema("Planet",
                        name={"data_type": "Long", "cardinality": "SINGLE"}
                        )

        :param label: vertex label name . example: Planet
        :param properties_schema: properties . example **{"name": {"data_type": "Long", "cardinality": "SINGLE"}}
        :return:

        property types : https://docs.janusgraph.org/basics/schema/#property-key-data-type
        """
        return self.create_schema("edge", label, **properties_schema)

    def create_vertex_label_with_schema(self, label, **properties_schema):
        """

        property types : https://docs.janusgraph.org/basics/schema/#property-key-data-type

        :param label: vertex label name . example: Planet
        :param properties_schema: properties . example **{"name": {"data_type": "Long", "cardinality": "SINGLE"}}
        :return:
        """
        return self.create_schema("vertex", label, **properties_schema)

    def update_property_name(self, old_name, new_name):
        query_string = """
mgmt = graph.openManagement()
{old_name} = mgmt.getPropertyKey('{old_name}')
mgmt.changeName({old_name}, '{new_name}')
mgmt.commit()        
        """.format(old_name=old_name, new_name=new_name)
        return self.gremlin_client.query(query_string, serialize_elements=False)

    def update_vertex_label(self, old_name, new_name):
        query_string = """
mgmt = graph.openManagement()
{old_name} = mgmt.getVertexLabel('{old_name}')
mgmt.changeName({old_name}, '{new_name}')
mgmt.commit()        
        """.format(old_name=old_name, new_name=new_name)
        return self.gremlin_client.query(query_string, serialize_elements=False)

    def update_edge_label(self, old_name, new_name):
        query_string = """
mgmt = graph.openManagement()
{old_name} = mgmt.getEdgeLabel('{old_name}')
mgmt.changeName({old_name}, '{new_name}')
mgmt.commit()        
        """.format(old_name=old_name, new_name=new_name)
        return self.gremlin_client.query(query_string, serialize_elements=False)


class SchemaOperations(SchemaReadOperations, SchemaCreateUpdateOperations):
    pass
