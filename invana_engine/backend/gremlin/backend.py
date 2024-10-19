from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.io.graphsonV3d0 import GraphSONReader
from gremlin_python.process.graph_traversal import GraphTraversalSource
import typing
from ..base import BackendAbstract
from .serializer import INVANA_DESERIALIZER_MAP
from invana_engine.core.queries import Query


class GremlinBackend(BackendAbstract):

    connection_uri: typing.AnyStr = None
    traversal_source: typing.AnyStr = None
    deserializer_map: typing.Dict[str, typing.Any] = None
    g: GraphTraversalSource = None

    def __init__(self, connection_uri, traversal_source="g",
                 deserializer_map=None, default_timeout=None, *args, **kwargs):
        super().__init__(connection_uri, *args, **kwargs)
        self.traversal_source = traversal_source
        INVANA_DESERIALIZER_MAP.update(deserializer_map or {})
        self.deserializer_map = INVANA_DESERIALIZER_MAP


    def initiate_connector(self):
        self.connector = DriverRemoteConnection(
            self.connection_uri,
            traversal_source=self.traversal_source,
            graphson_reader=GraphSONReader(deserializer_map=self.deserializer_map),
            **self.transport_kwargs)
        self.g = traversal(
            traversal_source_class=self.graph_traversal_source_cls).withRemote(
            self.connection)
        

    def run_query(self, query_string: str, extra_options=None, timeout=None, **kwargs):
        if extra_options is None:
            extra_options = {} 
        # extra_options["evaluationTimeout"] = timeout if timeout else self.default_timeout
        # query_instance = Query(query_string, extra_options=extra_options )
        return self.connector.submit_async(query_string).result()
