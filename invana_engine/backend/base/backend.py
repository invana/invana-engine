
from abc import ABC, abstractmethod
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT

class BackendAbstract(ABC):

    connector = None

    def __init__(self, connection_uri, auth=None, default_timeout=None, *args, **kwargs):
        self.connector = connection_uri
        self.connector = None
        self.default_timeout = default_timeout if default_timeout else DEFAULT_QUERY_TIMEOUT
        self.initiate_connector()

    @abstractmethod
    def initiate_connector(self):
        """
        Abstract method to initiate the connector.
        This method must be implemented by any subclass.
        """

    @abstractmethod
    def run_query(self, query_string: str, extra_options=None, timeout=None, **kwargs):
        """
        Abstract method to make raw query on the database driver
        """
