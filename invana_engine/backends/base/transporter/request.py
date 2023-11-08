from invana_engine.utils.utils import create_uuid, get_elapsed_time, get_datetime
# from invana_engine.invana.helpers.utils import create_uuid, get_elapsed_time, get_datetime
from ....backends.base.transporter.constants import RequestStateTypes, QueryResponseErrorReasonTypes
from invana_engine.backends.base.events import ResponseReceivedButFailedEvent, ResponseReceivedSuccessfullyEvent, \
    RequestFinishedSuccessfullyEvent, RequestFinishedButFailedEvent, RequestStartedEvent, ServerDisconnectedErrorEvent, \
    RunTimeErrorEvent, ClientConnectorErrorEvent


class RequestBase:

    created_at = None
    request_id = None
    status_last_updated_at = None

    def __init__(self,  query: str, request_options: dict = None):
        self.setup_init()
        self.query = query
        self.request_options = request_options or {}
        self.started()

    def setup_init(self):
        self.request_id = create_uuid()
        self.created_at = get_datetime()
        self.status_last_updated_at = None

    def started(self):
        self.state = RequestStateTypes.STARTED
        self.update_last_updated_at()
        RequestStartedEvent(self)

    def get_elapsed_time(self):
        return get_elapsed_time(get_datetime(), self.created_at)

    def update_last_updated_at(self):
        self.status_last_updated_at = get_datetime()


class QueryRequest(RequestBase):

    def response_received_but_failed(self, message, exception: Exception):
        self.state = RequestStateTypes.RESPONSE_RECEIVED
        self.update_last_updated_at()
        ResponseReceivedButFailedEvent(self, message, exception)

    def response_received_successfully(self, status_code):
        self.state = RequestStateTypes.RESPONSE_RECEIVED
        self.update_last_updated_at()
        ResponseReceivedSuccessfullyEvent(self, status_code)

    def finished_with_failure(self, exception: Exception):
        self.state = RequestStateTypes.FINISHED
        self.update_last_updated_at()
        RequestFinishedButFailedEvent(self, exception)

    def finished_with_success(self):
        self.state = RequestStateTypes.FINISHED
        self.update_last_updated_at()
        RequestFinishedSuccessfullyEvent(self)

    def server_disconnected_error(self, e):
        self.state = RequestStateTypes.SERVER_DISCONNECTED
        self.update_last_updated_at()
        ServerDisconnectedErrorEvent(self, e)

    def runtime_error(self, e):
        self.state = RequestStateTypes.RUNTIME_ERROR
        self.update_last_updated_at()
        RunTimeErrorEvent(self, e)

    def client_connection_error(self, e):
        self.state = RequestStateTypes.CLIENT_CONNECTION_ERROR
        self.update_last_updated_at()
        ClientConnectorErrorEvent(self, e)
