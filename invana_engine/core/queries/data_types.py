from dataclasses import dataclass, field
from datetime import datetime
import typing as T
import uuid
from datetime import datetime
from .constants import QueryStateTypes
from invana_engine.utils.utils import create_uuid, get_elapsed_time, get_datetime


@dataclass
class QueryRequest:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    query_string: str
    extra_options: T.Dict = None

    def __repr__(self):
        return f"<Request:{self.id} query_string={self.query_string}>"


@dataclass
class QueryResponse:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    status_code: str = None
    data: T.Any = None
    error: T.Optional[Exception] = None

    def is_success(self):
        return False if self.error else True

    def __repr__(self):
        return f"<Response:{self.id} status_code={self.status_code}>"


@dataclass
class QueryEvent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    type: QueryStateTypes = None
    error: T.Optional[Exception] = None

    def __repr__(self):
        return f"<QueryEvent:{self.id} status_code={self.type}>"
