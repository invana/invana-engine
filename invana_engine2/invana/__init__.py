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

import logging
from invana_engine2.invana.graph import InvanaGraph
from invana_engine2.invana.gremlin.connector import GremlinConnector
from invana_engine2.invana.backends.janusgraph.connector \
    import JanusGraphConnector

logging.getLogger('asyncio').setLevel(logging.INFO)
logging.basicConfig(
    handlers=[logging.StreamHandler()],  # logging.FileHandler("job.log", mode='w'),
    format='[%(levelname)s:%(asctime)s:%(module)s.%(funcName)s:%(lineno)d] - %(message)s',
    level=logging.DEBUG
)
