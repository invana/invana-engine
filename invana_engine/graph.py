import logging
import importlib
from .backends.base import BackendAbstract
from .backends import GremlinBackend, CypherBackend
from .backends.exceptions import BackendNotFound
from invana_engine import settings


class InvanaGraph:

    backend : BackendAbstract
    backend_class_name: str = None
    
    def __init__(self):

        self.backend_class_name = settings.GRAPH_BACKEND_CLASS
        if self.backend_class_name == "CypherBackend":
            self.backend = CypherBackend(settings.GRAPH_BACKEND_URL, 
                                database_name=settings.GRAPH_BACKEND_DATABASE_NAME,
                                username=settings.GRAPH_BACKEND_AUTH_USERNAME,
                                password=settings.GRAPH_BACKEND_AUTH_PASSWORD,
                            )
        elif self.backend_class_name == "GremlinBackend":
              self.backend = GremlinBackend(settings.GRAPH_BACKEND_URL, 
                                    database_name=settings.GRAPH_BACKEND_DATABASE_NAME,
                                    username=settings.GRAPH_BACKEND_AUTH_USERNAME,
                                    password=settings.GRAPH_BACKEND_AUTH_PASSWORD,
                                    traversal_source=settings.GRAPH_BACKEND_GREMLIN_TRAVERSAL_SOURCE
                                )
        else:
            raise BackendNotFound(f"{self.backend_class_name} backend not found.")
        
    def connect(self):
        return self.backend.connect()

    def close(self):
        return self.backend.close()

    def reconnect(self):
        return self.backend.reconnect()

    # def get_backend_class(self, backend_class_name):
    #     # backend_module_str = ".".join(backend_cls_str.split(".")[:-1])
    #     # backend_class_name = backend_cls_str.split(".")[-1]
    #     # backend_module = importlib.import_module(backend_module_str)
    #     backend_module = importlib.import_module('invana_engine.backends')

    #     return getattr(backend_module, backend_class_name)
  
  
    def run_query(
            self,
            query_string: str,
            query_language=None,
            timeout: int = None,
            raise_exception: bool = False,
            finished_callback=None) -> any:
        """
        :param query:
        :param timeout:
        :param raise_exception: When set to False, no exception will be raised.
        :param finished_callback:
        :return:
        """
        return self.backend.run_query(
            query_string,
            query_language=query_language,
            timeout=timeout,
            raise_exception=raise_exception,
            finished_callback=finished_callback)

    def drop(self):
        logging.info("Dropping the data")
        self.backend.drop()