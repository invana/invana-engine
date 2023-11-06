
class InvanaGraph:

    def __init__(self, connection_uri: str, backend="janusgraph", auth=None):
        pass

    def connect(self):
        pass

    def close(self):
        pass

    def reconnect(self):
        pass

    def execute_query(self, query: str, timeout: int = None, raise_exception: bool = False,
                      finished_callback=None) -> any:
        """
        :param query:
        :param timeout:
        :param raise_exception: When set to False, no exception will be raised.
        :param finished_callback:
        :return:
        """
        pass
 