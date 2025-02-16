import typing as T
from abc import ABC, abstractmethod
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT
from ...core.queries import QueryResponse, QueryEvent, QueryRequest

class BackendAbstract(ABC):

    connection_uri: T.AnyStr = None
    driver = None
    is_readonly : bool = False

    def __init__(self, connection_uri, auth=None, 
                 is_readonly=None,
                default_timeout=DEFAULT_QUERY_TIMEOUT, *args, **kwargs):
        self.connection_uri = connection_uri
        self.driver = None
        self.is_readonly = is_readonly
        self.default_timeout = default_timeout if default_timeout else DEFAULT_QUERY_TIMEOUT
        # self.connect() this should be called after init

    @abstractmethod
    def connect(self):
        """
        Abstract method to initiate the driver.
        This method must be implemented by any subclass.
        """
    
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def reconnect(self):
        pass
    
    @abstractmethod
    def run_query(self, query_string: str, extra_options=None, timeout=None,
                  callback=None, finished_callback=None, **kwargs) -> QueryResponse:
        """
        Abstract method to make raw query on the database driver
        """

    @abstractmethod
    def drop(self):
        pass