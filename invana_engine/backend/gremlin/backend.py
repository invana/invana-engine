from gremlin_python.process.anonymous_traversal import traversal
# from .driver import DriverRemoteConnection
from gremlin_python.structure.io.graphsonV3d0 import GraphSONReader, GraphSONWriter
from gremlin_python.process.graph_traversal import GraphTraversalSource
import typing as T
from ..base import BackendAbstract
from .serializer import INVANA_DESERIALIZER_MAP
from invana_engine.core.queries import Query
from .traversal_source import InvanaTraversalSource
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


class GremlinBackend(BackendAbstract):

    connection_uri: T.AnyStr = None
    traversal_source: T.AnyStr = InvanaTraversalSource
    deserializer_map: T.Dict[str, T.Any] = None
    g: GraphTraversalSource = None
    call_from_event_loop: bool = False
    transport_kwargs: T.Dict = {} 

    def __init__(self, connection_uri, traversal_source="g",
                deserializer_map=None, default_timeout=None,
                call_from_event_loop=True,
                *args, **kwargs):
        super().__init__(connection_uri, default_timeout=default_timeout, *args, **kwargs)
        self.traversal_source = traversal_source if traversal_source else "g"
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
        self.g = traversal().withRemote(self.driver)
        

    def run_query(self, query_string: str, extra_options=None, timeout=None,
                  callback=None, finished_callback=None, **kwargs):
        if extra_options is None:
            extra_options = {} 
        extra_options["evaluationTimeout"] = timeout if timeout else self.default_timeout
        # query_instance = Query(query_string, extra_options=extra_options )
        _ = self.driver.submit_async(query_string).result()
        return _
     
