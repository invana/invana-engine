from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection as _DriverRemoteConnection
from invana_engine.core.queries import Query, QueryRequest, QueryResponse
from concurrent.futures import Future
from gremlin_python.driver.remote_connection import (
     RemoteTraversal)
from .utils import read_from_result_set_with_out_callback
from .traversal_source import InvanaTraversalSource


class DriverRemoteConnection(_DriverRemoteConnection):
    
    # @property
    # def client(self):
    #     return self._client
    pass


 
    # def _submit_async(self, bytecode):
    #     # log.debug("submit_async with bytecode '%s'", str(bytecode))
    #     future = Future()
    #     future_result_set = self._client.submit_async(bytecode).result()

    #     def cb(f):
    #         try:
    #             result_set = f.result()
    #             results = result_set.all().result()
    #             future.set_result(RemoteTraversal(iter(results)))
    #         except Exception as e:
    #             future.set_exception(e)

    #     future_result_set.add_done_callback(cb)
    #     return future

    # def submit_async(self, bytecode):
    #     # if request_options is None:
    #     #     request_options = {}
    #     # request_options.update(self._extract_request_options(bytecode))
    #     query_instance = Query(str(bytecode))
    #     try:
    #         response = self.submit_async(bytecode).result()
    #         response_instance = QueryResponse(data=response, status_code=200,)
    #         query_instance.add_response(response_instance)
    #         return response_instance
    #     except Exception as e:
    #         response_instance = QueryResponse(data=None, error=e, status_code=400,)
    #         query_instance.add_response(response_instance)
    #         return response_instance
    
    # def _submit_async(self, bytecode, query_instance):
    #     result_set = self._client.submit_async(bytecode, request_options=self._extract_request_options(bytecode))
    #     return  read_from_result_set_with_out_callback(result_set, query_instance)

    # def submit_async(self, bytecode):
    #     # if request_options is None:
    #     #     request_options = {}
    #     # request_options.update(self._extract_request_options(bytecode))
    #     query_instance = Query(str(bytecode))
    #     try:
    #         response = self._submit_async(bytecode, query_instance)
    #         response_instance = QueryResponse(data=response, status_code=200,)
    #         query_instance.add_response(response_instance)
    #         return response_instance
    #     except Exception as e:
    #         response_instance = QueryResponse(data=None, error=e, status_code=400,)
    #         query_instance.add_response(response_instance)
    #         return response_instance
        
