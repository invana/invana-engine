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
from invana_engine.core.queries import QueryResponse, Query
from invana_engine.types import RelationShip

# def read_from_result_set_with_callback(result_set, callback, query: Query, finished_callback):
#     def cb(f):
#         try:
#             f.result()
#         except Exception as e:
#             raise e
#         else:
#             while not result_set.stream.empty():
#                 single_result = result_set.stream.get_nowait()
#                 response_instance = QueryResponse(data=single_result, status_code=206)
#                 callback(response_instance)
#                 query.add_response(response_instance)
#                 query.response_received_successfully(206)
#             query.query_successful()

#     result_set.done.add_done_callback(cb)

#     if finished_callback:
#         finished_callback()


def read_from_result_set_with_out_callback(result_set, query_instance: Query=None):
    future = Future()

    def cb(f):
        try:
            f.result()
        except Exception as e:
            future.set_exception(e)
        else:
            results = []
            while not result_set.stream.empty():
                results += result_set.stream.get_nowait()
            response_instance = QueryResponse(data=results, status_code= 200)
            query_instance.query_successful(response_instance)
            future.set_result(response_instance)

    result_set.done.add_done_callback(cb)
    return future.result()

def get_id(_id):
    if isinstance(_id, dict):
        if isinstance(
                _id.get('@value'),
                dict) and _id.get("@value").get('relationId'):
            return _id.get('@value').get('relationId')
        else:
            return _id.get('@value')
    return _id



def divide_chunks(l, n):
    return [l[i * n:(i + 1) * n] for i in range((len(l) + n - 1) // n)]

import typing as T
if T.TYPE_CHECKING:
    from invana_engine.graph import InvanaGraph

def get_vertex_properties_of_edges(edges, graph: 'InvanaGraph'):
    """
    TODO - move this to gremlin
    By default, edge json will not have inv and outv properties,
    this method will fetch and stitch the fill vertex details to the edge inv and outv
    """

    nodes_map = {}

    vertex_ids = []
    for edge in edges:
        if not isinstance(edge, RelationShip):
            raise Exception("relationship data should be RelationShip type")
        vertex_ids.append(edge.inV.id)
        vertex_ids.append(edge.outV.id)
    unique_vertex_ids = list(set(vertex_ids))
    vertex_instances = graph.backend.objects.search_v(
        has__id__within=unique_vertex_ids).to_list()

    vertices_dict = dict([(v.id, v) for v in vertex_instances])
    
    for edge in edges:
        edge.inV_back = edge.inV
        edge.inV = vertices_dict[edge.inV.id]
        edge.outV_back = edge.outV
        edge.outV = vertices_dict[edge.outV.id]
        # creating unique nodes map
        nodes_map[edge.inV.id] = vertices_dict[edge.inV.id]
        nodes_map[edge.outV.id] = vertices_dict[edge.outV.id]
    return {"nodes": [datum.to_json() for datum in  list(nodes_map.values())],
            "edges": [datum.to_json() for datum in  edges]}
