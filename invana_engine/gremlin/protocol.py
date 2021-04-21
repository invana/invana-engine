from gremlin_python.driver.protocol import GremlinServerWSProtocol, GremlinServerError
from gremlin_python.driver import request
from gremlin_python.driver.resultset import ResultSet

import base64


class InvanaGremlinServerWSProtocol(GremlinServerWSProtocol):

    def data_received(self, message, results_dict):
        # if Gremlin Server cuts off then we get a None for the message
        if message is None:
            raise GremlinServerError({
                'code': 500,
                'message': 'Server disconnected - please try to reconnect',
                'attributes': {}
            })

        message = self._message_serializer.deserialize_message(message)
        request_id = message['requestId']
        result_set = results_dict[request_id] if request_id in results_dict else ResultSet(None, None)
        status_code = message['status']['code']
        aggregate_to = message['result']['meta'].get('aggregateTo', 'list')
        data = message['result']['data']
        result_set.aggregate_to = aggregate_to
        if status_code == 407:
            auth = b''.join([b'\x00', self._username.encode('utf-8'),
                             b'\x00', self._password.encode('utf-8')])
            request_message = request.RequestMessage(
                'traversal', 'authentication',
                {'sasl': base64.b64encode(auth).decode()}
            )
            self.write(request_id, request_message)
            data = self._transport.read()
            # Allow recursive call for auth
            return self.data_received(data, results_dict)
        elif status_code == 204:
            result_set.stream.put_nowait([])
            del results_dict[request_id]
            return status_code
        elif status_code in [200, 206]:
            result_set.stream.put_nowait(data)
            if status_code == 200:
                result_set.status_attributes = message['status']['attributes']
                del results_dict[request_id]
            return status_code
        else:
            del results_dict[request_id]
            raise GremlinServerError(message["status"])
