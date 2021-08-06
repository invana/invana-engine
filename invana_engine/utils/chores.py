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

from importlib import import_module
import asyncio


def import_klass(klass_path_string):
    components = klass_path_string.split('.')
    module = import_module(".".join(components[0: (components.__len__() - 1)]))
    return getattr(module, components[-1])


def to_camel_case(snake_str):
    # https://stackoverflow.com/a/19053800
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])



#
# def get_unique_items(elements):
#     vertices = []
#     edges = []
#     existing_vertices = []
#     existing_edges = []
#
#     for elem in elements:
#         elem_type = elem.type
#         if elem_type == "g:Edge" and elem.id not in existing_edges:
#             existing_edges.append(elem.id)
#             edges.append(elem)
#         elif elem_type == "g:Vertex" and elem.id not in existing_vertices:
#             existing_vertices.append(elem.id)
#             vertices.append(elem)
#     return vertices + edges
