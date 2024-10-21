from dataclasses import dataclass, field
from datetime import datetime
import typing as T
import uuid
from datetime import datetime
from .constants import QueryStateTypes
from invana_engine.utils.utils import create_uuid, get_elapsed_time, get_datetime


@dataclass
class QueryRequest:
    query_string: str
    id: str = field(default_factory=lambda: str(create_uuid()))
    timestamp: datetime = field(default_factory=datetime.now)
    extra_options: T.Optional[T.Dict] = field(default_factory=dict)

    def __repr__(self):
        return f"<Request:{self.id} query_string={self.query_string}>"


@dataclass
class QueryResponse:
    status_code: str = None
    id: str = field(default_factory=lambda: str(create_uuid()))
    timestamp: datetime = field(default_factory=datetime.now)
    data: T.Optional[T.Dict] = field(default_factory=dict)
    error: T.Optional[Exception] = None

    def is_success(self):
        return False if self.error else True

    def __repr__(self):
        return f"<Response:{self.id} status_code={self.status_code}>"


@dataclass
class QueryEvent:
    error: T.Optional[Exception] = None
    type: QueryStateTypes = QueryStateTypes
    id: str = field(default_factory=lambda: str(create_uuid()))
    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self):
        return f"<QueryEvent:{self.id} status_code={self.type}>"
