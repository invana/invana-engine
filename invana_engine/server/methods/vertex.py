#  Copyright 2020 Invana
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http:www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from invana_engine.server import mutation_type
from invana_engine.server.pubsub import pubsub
import json


@mutation_type.field("createVertex")
async def resolve_create_vertex(info, **message):
    print("=====create vertex info", info)
    print("=====create vertex message", message)
    # await pubsub.publish(channel="chatroom", message=json.dumps(message))
    return True
