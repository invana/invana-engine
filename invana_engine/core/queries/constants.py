from enum import Enum


class QueryStateTypes(Enum):
    CREATED = "CREATED"
    STARTED = "STARTED"
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"

    @classmethod
    def get_allowed_types(cls):
        return [state.name for state in cls]

# class QueryEventTypes:
#     """
#     Lifecyle of the Query - all the events 
#     """
#     QUERY_CREATED = "QUERY_CREATED"
#     # all the events about the 
#     DB_REQUEST_STARTED = "DB_REQUEST_STARTED"
#     DB_CONNECTION_FAILURE = "DB_CONNECTION_FAILURE" # failed to start the query, server connection failure
#     DB_CONNECTION_DISCONNECTED = "DB_CONNECTION_DISCONNECTED" # lost network access while querying
#     DB_ERROR = "DB_ERROR" # server failed to respond to the query, any error
#     DB_RESPONSE_RECEIVED = "DB_RESPONSE_RECEIVED"  # this status can be many for async execution

#     SERIALIZER_ERROR = "SERIALIZER_ERROR" # failed on backend serializer
#     QUERY_SUCCESSFUL = "QUERY_SUCCESSFUL"
#     QUERY_FAILED = "QUERY_FAILED"
#     QUERY_FINISHED = "QUERY_FINISHED"

#     @classmethod
#     def get_allowed_types(cls):
#         return [k for k in list(cls.__dict__.keys()) if not k.startswith("__") and k.isupper()]

 
 