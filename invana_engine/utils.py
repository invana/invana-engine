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
from urllib.parse import urlparse
import socket
from graphql.language.ast import FragmentSpreadNode


def get_host(url):
    o = urlparse(url)
    return f"{o.scheme}://{o.netloc}"


def get_client_info():
    hostname = socket.gethostname()
    return {
        'host_name': hostname,
        'ip_address': socket.gethostbyname(hostname)
    }


def get_field_names(info):
    """
    https://github.com/graphql-python/graphene/issues/348#issuecomment-267717809
    Parses a query info into a list of composite field names.
    For example the following query:
        {
          carts {
            edges {
              node {
                id
                name
                ...cartInfo
              }
            }
          }
        }
        fragment cartInfo on CartType { whatever }

    Will result in an array:
        [
            'carts',
            'carts.edges',
            'carts.edges.node',
            'carts.edges.node.id',
            'carts.edges.node.name',
            'carts.edges.node.whatever'
        ]
    """

    fragments = info.fragments

    def iterate_field_names(prefix, field):
        name = field.name.value
        if isinstance(field, FragmentSpreadNode):
            _results = []
            new_prefix = prefix
            sub_selection = fragments[field.name.value].selection_set.selections
        else:
            _results = [prefix + name]
            new_prefix = prefix + name + "."
            if field.selection_set:
                sub_selection = field.selection_set.selections
            else:
                sub_selection = []
        for sub_field in sub_selection:
            _results += iterate_field_names(new_prefix, sub_field)
        return _results

    results = iterate_field_names('', info.field_nodes[0])
    print("results", results)
    fields = [item.split(f"{results[0]}.")[1] for item in results[1:]]
    properties = [item.split(f"properties.")[1] for item in fields[1:] if item.startswith("properties.")]
    data = {"fields": fields, "properties": properties, "label": results[0]}
    return data
