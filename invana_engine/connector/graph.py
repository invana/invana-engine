
from ..backends.gremlin.connector import GremlinConnector

class InvanaGraph:

    def __init__(self, connection_uri: str):
        self.backend = GremlinConnector(connection_uri)

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
