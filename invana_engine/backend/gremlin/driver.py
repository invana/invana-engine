from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection as _DriverRemoteConnection
from invana_engine.core.queries import Query

class DriverRemoteConnection(_DriverRemoteConnection):
    
    def submit_async(self, bytecode, request_options=None):
        if request_options is None:
            request_options = self._extract_request_options(bytecode)
        # query_instance = Query(str(bytecode), extra_options=request_options )
        return super()._client.submit_async( bytecode, request_options=request_options )
