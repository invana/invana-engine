
from abc import ABC, abstractmethod


class BackendAbstract(ABC):

    connector = None

    def __init__(self, connection_uri, auth=None, *args, **kwargs):
        self.connector = connection_uri
        self.connector = None
        self.initiate_connector()

    @abstractmethod
    def initiate_connector(self):
        """
        Abstract method to initiate the connector.
        This method must be implemented by any subclass.
        """

    @abstractmethod
    def run_query(self, query_string: str, timeout=None, **kwargs):
        """
        Abstract method to make raw query on the database driver
        """
