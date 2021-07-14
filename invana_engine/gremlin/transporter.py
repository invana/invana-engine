#  Copyright 2020 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from gremlin_python.driver.aiohttp.transport import AiohttpTransport as _AiohttpTransport
import asyncio


class AiohttpTransport(_AiohttpTransport):
    nest_asyncio_applied = True

    # Default heartbeat of 5.0 seconds.
    def __init__(self, call_from_event_loop=None, read_timeout=None, write_timeout=None, **kwargs):
        if call_from_event_loop is not None and call_from_event_loop and not AiohttpTransport.nest_asyncio_applied:
            """ 
                The AiohttpTransport implementation uses the asyncio event loop. Because of this, it cannot be called within an
                event loop without nest_asyncio. If the code is ever refactored so that it can be called within an event loop
                this import and call can be removed. Without this, applications which use the event loop to call gremlin-python
                (such as Jupyter) will not work.
            """
            print("====call_from_event_loop")
            import nest_asyncio
            nest_asyncio.apply()
            AiohttpTransport.nest_asyncio_applied = True

        # Start event loop and initialize websocket and client to None
        self._loop = asyncio.get_event_loop()
        self._websocket = None
        self._client_session = None

        # Set all inner variables to parameters passed in.
        self._aiohttp_kwargs = kwargs
        self._write_timeout = write_timeout
        self._read_timeout = read_timeout
        if "max_content_length" in self._aiohttp_kwargs:
            self._aiohttp_kwargs["max_msg_size"] = self._aiohttp_kwargs.pop("max_content_length")
        if "ssl_options" in self._aiohttp_kwargs:
            self._aiohttp_kwargs["ssl"] = self._aiohttp_kwargs.pop("ssl_options")
