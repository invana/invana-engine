from .edge import Edge
from .vertex import Vertex
from .stats import StatsOps
from .schema import SchemaOps
from .serializers.graphson_v3 import GraphSONV3Reader
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from invana_engine.settings import gremlin_traversal_source as _gremlin_traversal_source


class GremlinClient:
    """

    client = GremlinClient("ws://127.0.0.1:8182/gremlin")
    client.execute_query("g.V().limit(1).toList()")
    """

    def __init__(self, gremlin_server_url,
                 gremlin_traversal_source=None,
                 gremlin_server_username=None,
                 gremlin_server_password=None,
                 serializer=None,
                 transport_factory=None):
        if gremlin_server_url is None:
            raise Exception("Invalid gremlin_server_url. default: ws://127.0.0.1:8182/gremlin")
        self.connection = DriverRemoteConnection(
            gremlin_server_url,
            gremlin_traversal_source or _gremlin_traversal_source,
            username=gremlin_server_username,
            password=gremlin_server_password,
            transport_factory=transport_factory
        )
        self.g = traversal().withRemote(self.connection)
        self.serializer = serializer

    def execute_query(self, raw_query, serialize_elements=True):
        """

        :param raw_query: Gremlin query in plain string.
        :param serialize_elements: this will convert data GraphSON data into JSON
        :return:
        """
        result = self.connection._client.submit(raw_query).all().result()
        if serialize_elements is True:
            return self.serializer.serialize_data(result)
        return result


class InvanaEngineClient:
    """
    Usage:

    graph_client = InvanaEngineClient(gremlin_server_url="ws://127.0.0.1:8182/gremlin")
    """

    def __init__(self,
                 gremlin_server_url,
                 gremlin_traversal_source=None,
                 gremlin_server_username=None,
                 gremlin_server_password=None,
                 serializer=None,
                 transport_factory=None):
        serializer = serializer or GraphSONV3Reader()
        self.gremlin_server_url = gremlin_server_url
        self.gremlin_client = GremlinClient(gremlin_server_url=gremlin_server_url,
                                            gremlin_traversal_source=gremlin_traversal_source,
                                            gremlin_server_username=gremlin_server_username,
                                            gremlin_server_password=gremlin_server_password,
                                            serializer=serializer,
                                            transport_factory=transport_factory)
        self.vertex = Vertex(gremlin_client=self.gremlin_client)
        self.edge = Edge(gremlin_client=self.gremlin_client)
        self.stats = StatsOps(gremlin_client=self.gremlin_client)
        self.schema = SchemaOps(gremlin_client=self.gremlin_client)

    def close(self):
        self.gremlin_client.connection.close()

    def delete_everything(self):
        """

        :return: None
        """
        return self.gremlin_client.g.V().drop().iterate()

    def execute_query(self, raw_query, serialize_elements=True):
        """

        :param raw_query: Gremlin query in plain string.
        :param serialize_elements: this will convert data GraphSON data into JSON
        :return:
        """
        return self.gremlin_client.execute_query(raw_query, serialize_elements=serialize_elements)
