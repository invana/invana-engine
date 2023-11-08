from invana_engine.utils.utils import create_uuid, get_elapsed_time, get_datetime


class ResponseBase:

    request_id = None
    data = None
    status_code = None
    exception = None
    created_at = None

    def __init__(self, request_id, status_code, data=None, exception=None):
        self.request_id = request_id
        self.data = data
        self.status_code = status_code
        self.exception = exception
        self.created_at = get_datetime()

    def is_success(self):
        return False if self.exception else True

    def __repr__(self):
        return f"<Response:{self.request_id} status_code={self.status_code}>"


class QueryResponse(ResponseBase):
    pass
