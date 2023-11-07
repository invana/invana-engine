
class RequestStateTypes:
    STARTED = "STARTED"
    RESPONSE_RECEIVED = "RESPONSE_RECEIVED"  # this status can be many for async execution
    FINISHED = "FINISHED"
    SERVER_DISCONNECTED = "SERVER_DISCONNECTED"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    CLIENT_CONNECTION_ERROR = "CLIENT_CONNECTION_ERROR"

    @classmethod
    def get_allowed_types(cls):
        return [k for k in list(cls.__dict__.keys()) if not k.startswith("__") and k.isupper()]


class QueryResponseStatusTypes:
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    @classmethod
    def get_allowed_types(cls):
        return [k for k in list(cls.__dict__.keys()) if not k.startswith("__") and k.isupper()]


class QueryResponseErrorReasonTypes:
    # theses are error statuses when query response is received
    TIMED_OUT = "TIMED_OUT"
    INVALID_QUERY = "INVALID_QUERY"
    OTHER = "OTHER"

    @classmethod
    def get_allowed_types(cls):
        return [k for k in list(cls.__dict__.keys()) if not k.startswith("__") and k.isupper()]

