from invana_engine.settings import DEFAULT_QUERY_TIMEOUT, GRAPH_BACKEND_AUTH_USERNAME,  \
    GRAPH_BACKEND_AUTH_PASSWORD, GRAPH_BACKEND_DATABASE_NAME
from ..base import BackendAbstract
from invana_engine.core.queries import Query, QueryResponse, QueryRequest
from neo4j import GraphDatabase, RoutingControl
import logging
from .serializer import CypherSerializer
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT, GRAPH_BACKEND_URL, \
    GRAPH_BACKEND_AUTH_USERNAME, GRAPH_BACKEND_AUTH_PASSWORD, GRAPH_BACKEND_DATABASE_NAME
logger = logging.getLogger(__name__)


class CypherBackend(BackendAbstract):
    
    def __init__(self, 
                connection_uri: str,
                is_readonly=False, 
                default_timeout=DEFAULT_QUERY_TIMEOUT,
                database_name=GRAPH_BACKEND_DATABASE_NAME,
                username=GRAPH_BACKEND_AUTH_USERNAME,
                password=GRAPH_BACKEND_AUTH_PASSWORD,
                **kwargs) -> None:
        super().__init__(connection_uri=connection_uri, 
                        is_readonly=is_readonly, 
                        default_timeout=default_timeout, 
                      
                        **kwargs)
        self.database_name=database_name
        self.username=username
        self.password=password
        self.connect()


    def connect(self):
        logger.debug(f"create driver connection  ")
        self.driver =  GraphDatabase.driver(self.connection_uri, 
                            auth=(self.username, self.password))
     
    def reconnect(self):
        pass

    def close(self) -> None:
        self.driver.close()

    def drop(self):
        raise NotImplementedError()
    
    def serialize_response(self, records):
        return CypherSerializer().serialize_response(records)

    def run_query(self, query_string: str, extra_options=None, 
                  timeout=None, callback=None, **kwargs):       

        query_instance = Query(query_string)
        query_instance.query_started()
        try:
            records, _, _ = self.driver.execute_query(
                query_string,
                database_=self.database_name,
                routing_=RoutingControl.READ if self.is_readonly is True else RoutingControl.WRITE,
            )
            results =  self.serialize_response(records)
            response_instance = QueryResponse(data=results, status_code=200)
            query_instance.query_successful(response_instance)
            return response_instance
        except Exception as e:
            query_instance.query_failed(e)
            raise e
        
        # return QueryResponse(request.request_id, 200, data=results)
    