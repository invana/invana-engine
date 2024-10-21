import logging
from .backend.base import BackendAbstract
from .backend import GremlinBackend
from .settings import GRAPH_BACKEND_URL


class InvanaGraph:

    backend : BackendAbstract
    
    def __init__(self):
        # self.settings = settings
        self.backend = GremlinBackend(GRAPH_BACKEND_URL)
  
    def connect(self):
        return self.backend.connect()

    def close(self):
        return self.backend.close()

    def reconnect(self):
        return self.backend.reconnect()

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