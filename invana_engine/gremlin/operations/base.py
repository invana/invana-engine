import abc
from ..core.exceptions import InvalidQueryArguments, InvalidPropertiesException
from ..core.translator import GremlinQueryTranslator


class GremlinOperationBase:

    def __init__(self, gremlin_client=None):
        """

        :param gremlin_client: InvanaEngineClient instance
        """
        self.gremlin_client = gremlin_client
        self.translator = GremlinQueryTranslator()

    # @staticmethod
    # def get_namespaced_label(label=None, namespace=None):
    #     return "{}/{}".format(namespace, label) if namespace else label

    @staticmethod
    def validate_properties(properties):
        if not isinstance(properties, dict):
            raise InvalidPropertiesException(
                "properties should be passed as 'dict' type, but received '{}' type".format(type(properties)))

    @property
    def serializer(self):
        return self.gremlin_client.serializer

    @staticmethod
    def process_graph_schema_string(schema_string):
        schema = {
            "vertex_labels": [],
            "edge_labels": [],
            "property_keys": [],
        }
        data_type = None
        __count = 0
        for line in schema_string.split("\n"):
            if line.startswith("-------"):
                __count += 1
                continue
            if data_type == "vertices" and __count == 2:
                schema['vertex_labels'].append(line.split("|")[0].strip())
            elif data_type == "edges" and __count == 4:
                schema['edge_labels'].append(line.split("|")[0].strip())
            elif data_type == "properties" and __count == 6:
                schema['property_keys'].append(line.split("|")[0].strip())

            if line.startswith("Vertex Label Name"):
                data_type = "vertices"
            elif line.startswith("Edge Label Name"):
                data_type = "edges"
            elif line.startswith("Property Key Name"):
                data_type = "properties"
        return schema

    def get_graph_schema(self):
        # TODO - can add more information from the print schema data like indexes etc to current output
        result = self.gremlin_client.query("mgmt = graph.openManagement(); mgmt.printSchema()")
        return self.process_graph_schema_string(result[0])


class CRUDOperationsBase(GremlinOperationBase, metaclass=abc.ABCMeta):
    pass
