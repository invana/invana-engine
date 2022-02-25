#  Copyright 2021 Invana
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#  http:www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
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
import uvicorn
from invana_engine.server.app import app
import logging
from invana_engine.settings import server_port, shall_debug

if shall_debug is False:
    logging.getLogger('asyncio').setLevel(logging.ERROR)
    logging.getLogger('uvicorn').setLevel(logging.ERROR)
else:
    logging.basicConfig(level="DEBUG")


def server_start():
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))


if __name__ == "__main__":
    server_start()
