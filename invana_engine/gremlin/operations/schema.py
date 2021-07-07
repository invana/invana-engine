from .base import CRUDOperationsBase
import logging

logger = logging.getLogger(__name__)


class SchemaReadOperations(CRUDOperationsBase):

    def get_graph_schema(self):
        # TODO - can add more information from the print schema data like indexes etc to current output
        result = self.gremlin_client.query("mgmt = graph.openManagement(); mgmt.printSchema()")
        return self.process_graph_schema_string(result[0])

    def get_all_vertices_schema(self):
        # TODO - fix performance, this query needs full scan of the graph
        _ = self.gremlin_client.query("g.V().group().by(label).by(properties().label().dedup().fold())",
                                      serialize_elements=False)
        schema_data = []
        for schema in _:
            for k, v in schema.items():
                schema_data.append({"label": k, "propertyKeys": v})
        return schema_data

    def get_all_edges_schema(self):
        # TODO - fix performance, this query needs full scan of the graph
        _ = self.gremlin_client.query("g.E().group().by(label).by(properties().label().dedup().fold())",
                                      serialize_elements=False)
        schema_data = []
        for schema in _:
            for k, v in schema.items():
                schema_data.append({"label": k, "propertyKeys": v})
        return schema_data

    def get_vertex_schema(self, label):
        schema_data = self.get_all_vertices_schema()
        for label_schema in schema_data:
            if label_schema['label'] == label:
                return label_schema
        return

    def get_edge_schema(self, label):
        schema_data = self.get_all_edges_schema()
        for label_schema in schema_data:
            if label_schema['label'] == label:
                return label_schema
        return


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

        property types : https://docs.janusgraph.org/basics/schema/#property-key-data-type

        :param label: vertex label name . example: Planet
        :param properties_schema: properties . example **{"name": {"data_type": "Long", "cardinality": "SINGLE"}}
        :return:
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


class SchemaOperations(SchemaReadOperations, SchemaCreateUpdateOperations):
    pass
