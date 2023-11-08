#    Copyright 2021 Invana
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#     http:www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from gremlin_python.driver.protocol import GremlinServerError
# from invana_engine.invana.helpers.utils import create_uuid, get_elapsed_time, get_datetime
from ..constants import  GremlinServerErrorStatusCodes
from ....backends.base.transporter.constants import RequestStateTypes, QueryResponseErrorReasonTypes
from invana_engine.backends.base.events import ResponseReceivedButFailedEvent, ResponseReceivedSuccessfullyEvent, \
    RequestFinishedSuccessfullyEvent, RequestFinishedButFailedEvent, RequestStartedEvent, ServerDisconnectedErrorEvent, \
    RunTimeErrorEvent, ClientConnectorErrorEvent
from invana_engine.backends.base.transporter import QueryRequest



class GremlinQueryRequest(QueryRequest):
    state = None
    status_last_updated_at = None

    def __repr__(self):
        return f"<GremlinQueryRequest {self.request_id}>"

    def response_received_but_failed(self, exception: GremlinServerError):
        self.state = RequestStateTypes.RESPONSE_RECEIVED
        self.update_last_updated_at()
        if hasattr(exception, "status_code"):
            error_reason = None
            gremlin_server_error = None
            if exception.status_code == 597:
                gremlin_server_error = getattr(GremlinServerErrorStatusCodes, f"ERROR_{exception.status_code}")
                error_reason = QueryResponseErrorReasonTypes.INVALID_QUERY
                ResponseReceivedButFailedEvent(self, exception.status_code, exception)
        else:
            ResponseReceivedButFailedEvent(self, "", exception)

 