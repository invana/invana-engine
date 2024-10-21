from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.structure.io.graphsonV3d0 import GraphSONReader, GraphSONWriter
from gremlin_python.process.graph_traversal import GraphTraversalSource
import typing as T
from ..base import BackendAbstract
from .serializer import INVANA_DESERIALIZER_MAP
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT
from invana_engine.core.queries import Query, QueryResponse, QueryRequest
from .traversal_source import InvanaTraversalSource
# from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from .driver import DriverRemoteConnection
from .utils import read_from_result_set_with_out_callback


class GremlinBackend(BackendAbstract):

    traversal_source: T.AnyStr = "g"
    traversal_source_class: GraphTraversalSource = InvanaTraversalSource
    deserializer_map: T.Dict[str, T.Any] = None
    g: GraphTraversalSource = InvanaTraversalSource
    call_from_event_loop: bool = False
    transport_kwargs: T.Dict = {} 

    def __init__(self, connection_uri, 
                 traversal_source="g",
                deserializer_map=None, 
                is_readonly=False,
                default_timeout=DEFAULT_QUERY_TIMEOUT,
                traversal_source_class=InvanaTraversalSource,
                call_from_event_loop=True,
                *args, **kwargs):
        super().__init__(connection_uri, 
                         default_timeout=default_timeout,
                        is_readonly=is_readonly,  
                        *args, **kwargs)
        self.traversal_source = traversal_source if traversal_source else "g"
        self.traversal_source_class = traversal_source_class
        INVANA_DESERIALIZER_MAP.update(deserializer_map or {})
        self.call_from_event_loop = call_from_event_loop
        self.deserializer_map = INVANA_DESERIALIZER_MAP
        if call_from_event_loop:
            self.transport_kwargs['call_from_event_loop'] = call_from_event_loop
        self.connect()

    def connect(self):
        self.driver = DriverRemoteConnection(
                self.connection_uri,
                traversal_source=self.traversal_source,
                graphson_reader=GraphSONReader(deserializer_map=self.deserializer_map),
                graphson_writer=GraphSONWriter(serializer_map={}),
                **self.transport_kwargs
            )
        self.g = traversal(traversal_source_class=self.traversal_source_class).withRemote(self.driver)
        
    def close(self):
        pass

    def reconnect(self):
        pass

    def run_query(self, query_string: str, extra_options=None, timeout=None,
                  callback=None, finished_callback=None, **kwargs):
        if extra_options is None:
            extra_options = {} 
        extra_options["evaluationTimeout"] = timeout if timeout else self.default_timeout
        query_instance = Query(str(query_string), extra_options=extra_options)
        query_instance.query_started()
        try:
            result_set = self.driver._client.submit_async(query_string, request_options=extra_options).result()
            response_instance = read_from_result_set_with_out_callback(result_set, query_instance)
            query_instance.query_successful(response_instance)
            return response_instance
        except Exception as e:
            response_instance = QueryResponse(data=None, error=e, status_code=400,)
            query_instance.query_failed(response_instance, error=e)
            return response_instance
   
    def drop(self):
        self.g.V().drop().iterate()