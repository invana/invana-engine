from ..base.connector import ConnectorBase
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT
from aiohttp import ServerDisconnectedError, ClientConnectorError
from gremlin_python.structure.io.graphsonV3d0 import GraphSONReader
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.strategies import ReadOnlyStrategy
from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection as _DriverRemoteConnection
from .traversal.traversal_source import InvanaTraversalSource
from .serializer.graphson_reader import INVANA_DESERIALIZER_MAP
from .transporter.request import GremlinQueryRequest
from .constants import GremlinServerErrorStatusCodes
from .transporter.response import GremlinQueryResponse
from .utils import read_from_result_set_with_callback, read_from_result_set_with_out_callback
import logging

logger = logging.getLogger(__name__)

class DriverRemoteConnection(_DriverRemoteConnection):

    @property
    def client(self):
        return self._client


class GremlinConnector(ConnectorBase):

    def __init__(self, connection_uri: str, 
                is_readonly=False, 
                default_timeout=None,
                default_query_language="gremlin",
                database_name=None,
                username=None,
                password=None,
                traversal_source="g",
                strategies=None,
                graph_traversal_source_cls=InvanaTraversalSource, 
                call_from_event_loop=True,
                deserializer_map=None,
                **transport_kwargs) -> None:
        super().__init__(connection_uri, is_readonly=is_readonly,
                        default_query_language=default_query_language,
                        database_name=database_name,
                        username=username,
                        password=password,
                        default_timeout=default_timeout, **transport_kwargs)
        self.g = None
        self.traversal_source = traversal_source
        self.graph_traversal_source_cls =  graph_traversal_source_cls
        self.strategies = strategies or []
        if is_readonly:
            self.strategies.append(ReadOnlyStrategy())
        self.transport_kwargs = transport_kwargs

        if call_from_event_loop:
            transport_kwargs['call_from_event_loop'] = call_from_event_loop
        INVANA_DESERIALIZER_MAP.update(deserializer_map or {})
        self.deserializer_map = INVANA_DESERIALIZER_MAP
        self.connect()

    def supported_query_languages(self):
        return ["gremlin"]

    def _init_connection(self):
        logger.debug(f"create driver connection  ")
        self.connection = DriverRemoteConnection(
            self.connection_uri,
            traversal_source=self.traversal_source,
            graphson_reader=GraphSONReader(deserializer_map=self.deserializer_map),
            **self.transport_kwargs
        )
        self.g = traversal(traversal_source_class=self.graph_traversal_source_cls).withRemote(self.connection)
        if self.strategies.__len__() > 0:
            self.g = self.g.withStrategies(*self.strategies)
        # import time 
        # time.sleep(1)

    def _close_connection(self) -> None:
        self.connection.client.close()
 
  
    def convert_strategies_object_to_string(self) -> str:
        graph_strategies_str = "g.withStrategies("
        for strategy in self.strategies:
            strategy_kwargs = ""
            for k, v in strategy.__dict__['configuration'].items():
                strategy_kwargs += f"{k}:'{v}'," if type(v) is str else f"{k}:{v},"
            strategy_kwargs = strategy_kwargs.rstrip(",")
            graph_strategies_str += f"new {strategy.__dict__['strategy_name']}({strategy_kwargs})"
        graph_strategies_str += ")."
        return graph_strategies_str

    def add_strategies_to_query(self, query_string):
        if self.strategies.__len__() > 0:
            strategy_prefix = self.convert_strategies_object_to_string()
            query_string = query_string.replace("g.", strategy_prefix, 1)
        return query_string

    def get_features(self):
        response = self.execute_query("graph.features()")
        lines = response.data[0].lstrip("FEATURES\n").split("> ")
        data = {}
        for line in lines[1:]:
            items = line.rstrip().split("\n")
            data[items[0]] = {}
            for item in items[1:]:
                item = item.lstrip(">-- ").split(":")
                data[items[0]][item[0].strip()] = bool(item[1])
        response.data = data
        return response
    
    @staticmethod
    def process_error_exception(exception: GremlinServerError):
        gremlin_server_error = getattr(GremlinServerErrorStatusCodes, f"ERROR_{exception.status_code}")
        return exception.status_code, gremlin_server_error

    def serialize_response(self):
        pass

    def _execute_query(self, query: str,
                       timeout: int = None,
                       query_language = None,
                       callback=None,
                       finished_callback=None,
                       raise_exception: bool = False) -> any:
        """

        :param query:
        :param timeout:
        :param callback:
        :param finished_callback:
        :param raise_exception: When set to False, no exception will be raised.
        :return:
        """
        query_language = query_language if query_language else self.default_query_language
        query_string = self.add_strategies_to_query(query)
        timeout = timeout if timeout else self.default_timeout
        request_options = {"evaluationTimeout": timeout}
        request = GremlinQueryRequest(query)
        try:
            result_set = self.connection.client.submitAsync(query_string, request_options=request_options).result()
            if callback:
                read_from_result_set_with_callback(result_set, callback, request, finished_callback=finished_callback)
            else:
                response = read_from_result_set_with_out_callback(result_set, request)
                if finished_callback:
                    finished_callback()
                return response
        except GremlinServerError as e:
            request.response_received_but_failed(e)
            request.finished_with_failure(e)
            status_code, gremlin_server_error = self.process_error_exception(e)
            e.args = [f"Failed to execute {request} with reason: {status_code}:{gremlin_server_error}"
                      f" and error message {e.__str__()}"]
            if raise_exception is True:
                raise e
            return GremlinQueryResponse(request.request_id, 500, exception=e)
        except ServerDisconnectedError as e:
            request.server_disconnected_error(e)
            request.finished_with_failure(e)
            if raise_exception is True:
                raise Exception(f"Failed to execute {request} with error message {e.__str__()}")
            return GremlinQueryResponse(request.request_id, 500, exception=e)
        except RuntimeError as e:
            e.args = [f"Failed to execute {request} with error message {e.__str__()}"]
            request.runtime_error(e)
            request.finished_with_failure(e)
            if raise_exception is True:
                raise e
            return GremlinQueryResponse(request.request_id, None, exception=e)
        except ClientConnectorError as e:
            e.args = [f"Failed to execute {request} with error message {e.__str__()}"]
            request.client_connection_error(e)
            request.finished_with_failure(e)
            if raise_exception is True:
                raise e
            return GremlinQueryResponse(request.request_id, 500, exception=e)
        except Exception as e:
            e.args = [f"Failed to execute {request} with error message {e.__str__()}"]
            request.response_received_but_failed(e)
            request.finished_with_failure(e)
            if raise_exception is True:
                raise e
            return GremlinQueryResponse(request.request_id, None, exception=e)

 