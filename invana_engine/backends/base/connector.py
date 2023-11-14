import abc
import logging
from .constants import ConnectionStateTypes
from invana_engine.settings import DEFAULT_QUERY_TIMEOUT
from .exceptions import InvalidDefaultQueryLanguageException
import typing
logger = logging.getLogger(__name__)


class ConnectorBase(abc.ABC):


    def __init__(self, connection_uri:str, is_readonly:  typing.Optional[bool]=False,
                default_timeout:  typing.Optional[int]=DEFAULT_QUERY_TIMEOUT,
                database_name:  typing.Optional[str]=None,
                username: typing.Optional[str]=None,
                password:  typing.Optional[str]=None,
                default_query_language:  typing.Optional[str]=None,
                **kwargs ) -> None:
        self.CONNECTION_STATE = None
        self.connection_uri = connection_uri
        self.is_readonly = is_readonly
        self.database_name = database_name
        self.username = username
        self.password = password

        self.default_query_language = default_query_language
        self.validate_query_language(self.default_query_language)
        self.default_timeout = default_timeout

    @abc.abstractmethod
    def supported_query_languages(self):
        pass

    def validate_query_language(self, query_language):
        if query_language not in self.supported_query_languages():
            raise InvalidDefaultQueryLanguageException(
                f"{query_language} is not among {self.supported_query_languages()}")

    def get_basic_info(self):
        return {
            "connection_uri" : self.connection_uri,
            "backend_class": self.__class__.__name__, # type(self).__name__,
            "is_readonly": self.is_readonly,
            "default_query_language": self.default_query_language,
            "supported_query_languages": self.supported_query_languages()
        }

    def update_connection_state(self, new_state):
        self.CONNECTION_STATE = new_state
        logger.debug(f"GraphConnector state updated to : {self.CONNECTION_STATE}")

    @abc.abstractmethod
    def _init_connection(self):
        pass

    @abc.abstractmethod
    def _close_connection(self):
        pass    

    def connect(self):
        self.update_connection_state(ConnectionStateTypes.CONNECTING)
        self._init_connection()
        self.update_connection_state(ConnectionStateTypes.CONNECTED)

    def reconnect(self):
        self.update_connection_state(ConnectionStateTypes.RECONNECTING)
        self.connect()

    def close(self) -> None:
        self.update_connection_state(ConnectionStateTypes.DISCONNECTING)
        self._close_connection()
        self.update_connection_state(ConnectionStateTypes.DISCONNECTED)

    @abc.abstractmethod
    def serialize_response(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def _execute_query(self, query:str, timeout:int=None, serialize=True, raise_exception:bool= False, 
                       query_language=None, finished_callback=None ):
        pass

    def execute_query(self, query: str, timeout: int = None, raise_exception: bool = False,
                      query_language: str = None, 
                      finished_callback=None) -> any:
        """

        :param query:
        :param timeout:
        :param raise_exception: When set to False, no exception will be raised.
        :param finished_callback:
        :return:
        """
        query_language = query_language if query_language else self.default_query_language
        self.validate_query_language(self.default_query_language)
        return self._execute_query(query, timeout=timeout, raise_exception=raise_exception,
                                   query_language=query_language,
                                   finished_callback=finished_callback)
