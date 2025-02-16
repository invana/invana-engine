import typing as T
from abc import ABC, abstractmethod
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT
from ...core.queries import QueryResponse, QueryEvent, QueryRequest
if T.TYPE_CHECKING:
    from .queryset import GenericQuerySetAbstract, SchemaQuerySetAbstract


class BackendAbstract(ABC):

    connection_uri: T.AnyStr = None
    driver = None
    is_readonly : bool = False
    default_query_language: T.AnyStr = None

    # objects_cls : "GenericQuerySetAbstract"
    # schema_cls : "SchemaQuerySetAbstract"

    objects: "GenericQuerySetAbstract"  = None
    schema: "SchemaQuerySetAbstract"  = None

    def __init__(self, connection_uri, auth=None, 
                 is_readonly=None,
                default_timeout=DEFAULT_QUERY_TIMEOUT, *args, **kwargs):
        self.connection_uri = connection_uri
        self.driver = None
        self.is_readonly = is_readonly
        self.default_timeout = default_timeout if default_timeout else DEFAULT_QUERY_TIMEOUT
        # self.connect() this should be called after init
        # if self.objects_cls is None:
        #     raise NotImplementedError("objects_cls must be set in the Backend class") 
        # if self.schema_cls is None:
        #     raise NotImplementedError("schema_cls must be set in the Backend class")   
        # self.objects = self.objects_cls(self)
        # self.schema = self.schema_cls(self)

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

    def get_backend_info(self):
        return {
            "connection_uri" : self.connection_uri,
            "backend_class": self.__class__.__name__, # type(self).__name__,
            "is_readonly": self.is_readonly,
            "default_query_language": self.default_query_language,
            # "supported_query_languages": self.supported_query_languages()
        }

    @abstractmethod
    def drop(self):
        pass