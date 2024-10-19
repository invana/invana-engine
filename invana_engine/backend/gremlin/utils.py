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

from concurrent.futures import Future
from invana_engine.core.queries import QueryResponse
from functools import wraps


def read_from_result_set_decorator(func):
    @wraps(func)
    def wrapper(result_set, request, callback=None, finished_callback=None, *args, **kwargs):
        def cb(f):
            try:
                f.result()
            except Exception as e:
                if request.has_callback:
                    raise e
                else:
                    future.set_exception(e)
            else:
                if request.has_callback:
                    # With callback
                    while not result_set.stream.empty():
                        single_result = result_set.stream.get_nowait()
                        callback(
                            QueryResponse(
                                206,
                                data=single_result))
                        request.response_received_successfully(206)
                    request.finished_with_success()
                    if finished_callback:
                        finished_callback()
                else:
                    # Without callback
                    results = []
                    while not result_set.stream.empty():
                        results += result_set.stream.get_nowait()

                    future.set_result(
                        QueryResponse(
                            status_code=200,
                            data=results
                        )
                    )
                    request.response_received_successfully(200)
                    request.finished_with_success()

        if not request.has_callback:
            future = Future()

        result_set.done.add_done_callback(cb)

        if not request.has_callback:
            return future.result()

        # Invoke the original function
        return func(result_set, request, callback, finished_callback, *args, **kwargs)

    return wrapper


def get_id(_id):
    if isinstance(_id, dict):
        if isinstance(
                _id.get('@value'),
                dict) and _id.get("@value").get('relationId'):
            return _id.get('@value').get('relationId')
        else:
            return _id.get('@value')
    return _id
