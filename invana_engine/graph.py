
from invana_engine import settings
import importlib


class InvanaGraph:

    def __init__(self):
        # self.settings = settings
        self.backend_cls_str = settings.GRAPH_BACKEND
        backend_cls = self.get_backend_class(self.backend_cls_str)
        if self.backend_cls_str == "CypherConnector":
            self.backend = backend_cls(getattr(settings, "GRAPH_BACKEND_URL"), 
                                    database_name=getattr(settings,"GRAPH_BACKEND_DATABASE_NAME"),
                                    username=getattr(settings,"GRAPH_BACKEND_AUTH_USERNAME"),
                                    password=getattr(settings,"GRAPH_BACKEND_AUTH_PASSWORD"),
                                    )
        else:
            backend_cls = self.get_backend_class(self.backend_cls_str)
            self.backend = backend_cls(getattr(settings, "GRAPH_BACKEND_URL"), 
                                    database_name=getattr(settings,"GRAPH_BACKEND_DATABASE_NAME"),
                                    username=getattr(settings,"GRAPH_BACKEND_AUTH_USERNAME"),
                                    password=getattr(settings,"GRAPH_BACKEND_AUTH_PASSWORD"),
                                    traversal_source=getattr(settings, "GRAPH_BACKEND_GREMLIN_TRAVERSAL_SOURCE")
                                    )
        
     

    def get_backend_class(self, backend_cls_str):
        backend_module_str = "invana_engine.backends"
        if "." in backend_cls_str:
            backend_module_str = ".".join(backend_cls_str.split(".")[:-1])
            backend_class_name = backend_cls_str.split(".")[-1]
            backend_module = importlib.import_module(backend_module_str)
            return getattr(backend_module, backend_class_name)
        # default if expects to find the class in `invana_engine.backends`
        backend_module = importlib.import_module('invana_engine.backends')
        return getattr(backend_module, backend_cls_str)
  

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
