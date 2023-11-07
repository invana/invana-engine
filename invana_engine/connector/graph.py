
from ..backends import GremlinConnector, CypherConnector
from invana_engine import settings

class InvanaGraph:

    def __init__(self, backend_cls):
        # self.settings = settings

        if backend_cls == "CypherConnector":
            self.backend = CypherConnector(getattr(settings, "GRAPH_BACKEND_URL"), 
                                    database_name=getattr(settings,"GRAPH_BACKEND_DATABASE_NAME"),
                                    username=getattr(settings,"GRAPH_BACKEND_AUTH_USERNAME"),
                                    password=getattr(settings,"GRAPH_BACKEND_AUTH_PASSWORD"),
                                    )
        else:
            self.backend = GremlinConnector(getattr(settings, "GRAPH_BACKEND_URL"), 
                                    database_name=getattr(settings,"GRAPH_BACKEND_DATABASE_NAME"),
                                    username=getattr(settings,"GRAPH_BACKEND_AUTH_USERNAME"),
                                    password=getattr(settings,"GRAPH_BACKEND_AUTH_PASSWORD"),
                                    traversal_source=getattr(settings, "GRAPH_BACKEND_GREMLIN_TRAVERSAL_SOURCE")
                                    )
    

    def connect(self):
        return self.backend.connect()

    def close(self):
        return self.backend.close()

    def reconnect(self):
        return self.backend.reconnect()

    def execute_query(self, query_string: str, timeout: int = None, raise_exception: bool = False,
                      query_language=None,
                      finished_callback=None) -> any:
        """
        :param query:
        :param timeout:
        :param raise_exception: When set to False, no exception will be raised.
        :param finished_callback:
        :return:
        """
        return self.backend.execute_query(query_string, timeout=timeout, raise_exception=raise_exception,
                                          query_language=query_language,
                                             finished_callback=finished_callback)
