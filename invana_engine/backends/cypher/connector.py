from invana_engine.settings import DEFAULT_QUERY_TIMEOUT, GRAPH_BACKEND_AUTH_USERNAME,  \
    GRAPH_BACKEND_AUTH_PASSWORD, GRAPH_BACKEND_DATABASE_NAME
from ..base.connector import ConnectorBase
from ..base.transporter import QueryRequest, QueryResponse
from neo4j import GraphDatabase, RoutingControl
import logging
from .serializer import CypherSerializer
logger = logging.getLogger(__name__)


class CypherConnector(ConnectorBase):
    

    def __init__(self, connection_uri: str, is_readonly=False, default_timeout=None,
                default_query_language="cypher", 
                database_name=None,
                username=None,
                password=None,
                **kwargs) -> None:
        super().__init__(connection_uri=connection_uri, 
                        is_readonly=is_readonly, 
                        default_timeout=default_timeout, 
                        database_name=database_name,
                        username=username,
                        password=password,
                        default_query_language=default_query_language, **kwargs)
        self.connect()

    def supported_query_languages(self):
        return ["cypher"]

    def _init_connection(self):
        logger.debug(f"create driver connection  ")
        self.connection =  GraphDatabase.driver(self.connection_uri, 
                                                auth=(self.username, self.password))
        pass

    def _close_connection(self) -> None:
        self.connection.close()
 
    
    def serialize_response(self, records):
        
        return CypherSerializer().serialize_response(records)

    def _execute_query(self, query: str,
                       timeout: int = None,
                       query_language = None,
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
        

        request = QueryRequest(query)
        try:
            records, _, _ = self.connection.execute_query(
                query,
                database_=self.database_name,
                routing_=RoutingControl.READ if self.is_readonly is True else RoutingControl.WRITE,
            )
            results =  self.serialize_response(records)
            request.response_received_successfully(200)
            request.finished_with_success()
        except Exception as e:
            request.finished_with_failure(e)
            raise e
        return QueryResponse(request.request_id, 200, data=results)
    