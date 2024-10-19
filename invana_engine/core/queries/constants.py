from enum import Enum


class QueryStateTypes(Enum):
    CREATED = "CREATED"
    STARTED = "STARTED"
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"

    @classmethod
    def get_allowed_types(cls):
        return [state.name for state in cls]

 