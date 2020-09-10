from .edge import Edge
from .vertex import Vertex
from .core.serializer import GremlinResponseSerializer
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


class _GremlinClient:
    """

    client = _GremlinClient("ws://127.0.0.1:8182/gremlin")
    client.execute_query("g.V().limit(1).toList()")
    """

    def __init__(self, gremlin_server_url, serializer=None, transport_factory=None):
        if gremlin_server_url is None:
            raise Exception("Invalid gremlin_server_url. default: ws://127.0.0.1:8182/gremlin")
        self.connection = DriverRemoteConnection(
            gremlin_server_url, 'g',
            transport_factory=transport_factory
        )
        self.g = traversal().withRemote(self.connection)
        self.serializer = serializer

    def execute_query(self, raw_query):
        """

        :param raw_query: Gremlin query in plain string.
        :return:
        """
        result = self.connection._client.submit(raw_query).all().result()
        return self.serializer.serialize_data(result)


class GremlinClient:
    """
    Usage:

    graph_client = GremlinClient(gremlin_server_url="ws://127.0.0.1:8182/gremlin")
    """

    def __init__(self, gremlin_server_url, serializer=None, transport_factory=None):
        serializer = serializer or GremlinResponseSerializer()
        self.gremlin_server_url = gremlin_server_url
        self.gremlin_client = _GremlinClient(gremlin_server_url=gremlin_server_url,
                                             serializer=serializer,
                                             transport_factory=transport_factory)
        self.vertex = Vertex(gremlin_client=self.gremlin_client)
        self.edge = Edge(gremlin_client=self.gremlin_client)

    def close(self):
        self.gremlin_client.connection.close()

    def delete_everything(self):
        """

        :return: None
        """
        return self.gremlin_client.g.V().drop().iterate()

    def execute_query(self, raw_query):
        """

        :param raw_query: Gremlin query in plain string.
        :return:
        """
        return self.gremlin_client.execute_query(raw_query)
