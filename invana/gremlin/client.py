from .edge import Edge
from .vertex import Vertex
from .stats import StatsOps
from .schema import SchemaOps
from .serializers.graphson_v3 import GraphSONV3Reader
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.protocol import GremlinServerWSProtocol, GremlinServerError
from gremlin_python.driver import request
from gremlin_python.driver.resultset import ResultSet

import base64


class InvanaGremlinServerWSProtocol(GremlinServerWSProtocol):

    def data_received(self, message, results_dict):
        # if Gremlin Server cuts off then we get a None for the message
        if message is None:
            raise GremlinServerError({'code': 500,
                                      'message': 'Server disconnected - please try to reconnect', 'attributes': {}})

        message = self._message_serializer.deserialize_message(message)
        request_id = message['requestId']
        result_set = results_dict[request_id] if request_id in results_dict else ResultSet(None, None)
        status_code = message['status']['code']
        aggregate_to = message['result']['meta'].get('aggregateTo', 'list')
        data = message['result']['data']
        result_set.aggregate_to = aggregate_to
        if status_code == 407:
            auth = b''.join([b'\x00', self._username.encode('utf-8'),
                             b'\x00', self._password.encode('utf-8')])
            request_message = request.RequestMessage(
                'traversal', 'authentication',
                {'sasl': base64.b64encode(auth).decode()})
            self.write(request_id, request_message)
            data = self._transport.read()
            # Allow recursive call for auth
            return self.data_received(data, results_dict)
        elif status_code == 204:
            result_set.stream.put_nowait([])
            del results_dict[request_id]
            return status_code
        elif status_code in [200, 206]:
            result_set.stream.put_nowait(data)
            if status_code == 200:
                result_set.status_attributes = message['status']['attributes']
                del results_dict[request_id]
            return status_code
        else:
            del results_dict[request_id]
            raise GremlinServerError(message["status"])


class _GremlinClient:
    """

    client = _GremlinClient("ws://127.0.0.1:8182/gremlin")
    client.execute_query("g.V().limit(1).toList()")
    """

    def __init__(self, gremlin_server_url, gremlin_server_username=None,
                 gremlin_server_password=None, serializer=None, transport_factory=None):
        if gremlin_server_url is None:
            raise Exception("Invalid gremlin_server_url. default: ws://127.0.0.1:8182/gremlin")
        self.connection = DriverRemoteConnection(
            gremlin_server_url, 'g',
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


class GremlinClient:
    """
    Usage:

    graph_client = GremlinClient(gremlin_server_url="ws://127.0.0.1:8182/gremlin")
    """

    def __init__(self, gremlin_server_url, gremlin_server_username=None,
                 gremlin_server_password=None, serializer=None, transport_factory=None):
        serializer = serializer or GraphSONV3Reader()
        self.gremlin_server_url = gremlin_server_url
        self.gremlin_client = _GremlinClient(gremlin_server_url=gremlin_server_url,
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

    def execute_query(self, raw_query,  serialize_elements=True):
        """

        :param raw_query: Gremlin query in plain string.
        :param serialize_elements: this will convert data GraphSON data into JSON
        :return:
        """
        return self.gremlin_client.execute_query(raw_query,  serialize_elements=serialize_elements)
