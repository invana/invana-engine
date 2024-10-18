from abc import ABC, abstractmethod
from invana_engine.utils.utils import create_uuid, get_elapsed_time, get_datetime
from datetime import datetime
import typing as T
from .constants import QueryStateTypes
from .data_types import QueryResponse, QueryEvent, QueryRequest


class QueryBase:

    query_id = None
    parent_query_id = None

    _created_at = None
    _updated_at = None

    request = QueryRequest
    responses: T.List[QueryResponse]
    _state = None
    _events : T.List[QueryEvent] = []
    _runtime = None

    def __init__(self, 
                 query_string: str, 
                 extra_options: dict = None, 
                 parent_query_id: str = None):
        self.request = QueryRequest(query_string=query_string, extra_options=extra_options)
        self.query_id = create_uuid()
        self.parent_query_id = parent_query_id
        self._created_at = self.request.timestamp

    @abstractmethod
    def query_created(self):
        pass

    @property
    def updated_at(self):
        return self._updated_at
    
    @property
    def state(self):
        return self._state

    @property
    def events(self):
        return self._events
    
    @property
    def runtime(self):
        return self._runtime

    def get_event_by_state(self, state) -> QueryEvent:
        return next(filter(lambda item: item.type == state, self.events), None)

    def get_runtime(self):
        return self._runtime

    def updated_state(self, state: str, dt: datetime):
        self._updated_at = dt
        self._state = state

    def add_event(self, event: QueryEvent):
        self._events.append(event)
        self.updated_state(event.type, event.timestamp)
        if event.type == QueryStateTypes.FAILED:
            started_event = self.get_event_by_state(QueryStateTypes.STARTED)
            self._runtime = get_elapsed_time(event.timestamp - started_event.timestamp)
        elif event.type == QueryStateTypes.SUCCESSFUL:
            started_event = self.get_event_by_state(QueryStateTypes.STARTED)
            self._runtime = get_elapsed_time(event.timestamp - started_event.timestamp)


class Query(QueryBase):

    def query_created(self):
       self.add_event(QueryEvent(type=QueryStateTypes.CREATED, timestamp=self.request.timestamp))

    def query_started(self):
        self.add_event(QueryEvent(type=QueryStateTypes.STARTED))

    def query_successful(self, response: QueryResponse):
        self.add_event(QueryEvent(type=QueryStateTypes.SUCCESSFUL))

    def query_failed(self, e: Exception = None):
        self.add_event(QueryEvent(type=QueryStateTypes.SUCCESSFUL, error=e))