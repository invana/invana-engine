import logging
from invana_engine.utils.chores import import_klass
from invana_engine.default_settings import GREMLIN_SERVER_SETTINGS as GREMLIN_SERVER_DEFAULT_SETTINGS
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from .operations.vertex import VertexOperations
from .operations.edge import EdgeOperations


class GremlinClient:

    def __init__(self, server_url, traversal_source=None, serializer_class=None):
        if server_url is None:
            server_url = GREMLIN_SERVER_DEFAULT_SETTINGS['gremlin_url']
            logging.info("No server_url provided by user. using default value '{}'".format(server_url))
        if traversal_source is None:
            traversal_source = GREMLIN_SERVER_DEFAULT_SETTINGS['traversal_source']
            logging.info("No traversal_source provided by user. using default value '{}'".format(traversal_source))
        if serializer_class is None:
            serializer_class_str = GREMLIN_SERVER_DEFAULT_SETTINGS['serializer_class']
            logging.info("No serializer_class provided by user. using default serializer class '{}'".format(
                serializer_class_str))
            serializer_class = import_klass(serializer_class_str)

        self.server_url = server_url
        self.traversal_source = traversal_source
        self.serializer = serializer_class()
        # self.auth = auth
        self.connection = self.create_connection()
        self.g = traversal().withRemote(self.connection)
        self.vertex = VertexOperations(gremlin_client=self)
        self.edge = EdgeOperations(gremlin_client=self)

    def create_connection(self):
        return DriverRemoteConnection(
            self.server_url,
            self.traversal_source,
            # username=gremlin_server_username,
            # password=gremlin_server_password,
            # transport_factory=transport_factory
        )

    @staticmethod
    def make_data_unique(serialize_data):
        _ids = []
        unique_data = []
        for serialize_datum in serialize_data:
            if type(serialize_datum) is dict and serialize_datum.get("id"):
                if serialize_datum['id'] not in _ids:
                    _ids.append(serialize_datum['id'])
                    unique_data.append(serialize_datum)
            else:
                unique_data.append(serialize_datum)
        return unique_data

    def query(self, gremlin_query, serialize_elements=True):
        logging.info("gremlin_query======", gremlin_query)
        print("gremlin_query======", gremlin_query)
        try:
            result = self.connection._client.submit(gremlin_query).all().result()
        except Exception as e:
            logging.error("Failed to query gremlin server with exception: {}".format(e.__str__() if e else ""))
            print("Failed to query gremlin server with exception: {}".format(e.__str__() if e else ""))
            return None
        if serialize_elements is True:
            _ = self.make_data_unique(self.serializer.serialize_data(result))
            # _ = self.serializer.serialize_data(result)
            if isinstance(result, list):
                return _
            else:
                return _[0]
        return result

    def close_connection(self):
        self.connection.close()
