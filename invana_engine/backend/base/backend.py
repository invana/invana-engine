
from abc import ABC, abstractmethod
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT

class BackendAbstract(ABC):

    driver = None

    def __init__(self, connection_uri, auth=None, default_timeout=None, *args, **kwargs):
        self.connection_uri = connection_uri
        self.driver = None
        self.default_timeout = default_timeout if default_timeout else DEFAULT_QUERY_TIMEOUT
        # self.connect() this should be called after init

    @abstractmethod
    def connect(self):
        """
        Abstract method to initiate the driver.
        This method must be implemented by any subclass.
        """

    @abstractmethod
    def run_query(self, query_string: str, extra_options=None, timeout=None,
                  callback=None, finished_callback=None, **kwargs):
        """
        Abstract method to make raw query on the database driver
        """
