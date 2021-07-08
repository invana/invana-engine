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

from .base import CRUDOperationsBase
import logging
import json
from ..core.exceptions import InvalidQueryArguments
import ast

logger = logging.getLogger(__name__)


class CompositeIndexOperations(CRUDOperationsBase):

    @staticmethod
    def create_reindex_query(index_name):
        return """
mgmt = graph.openManagement()
mgmt.updateIndex(mgmt.getGraphIndex("{index_name}"), SchemaAction.REINDEX).get()
mgmt.commit()""".format(index_name=index_name)

    def create_vertex_index(self, index_name, label, property_keys):
        """

        :param index_name: unique index name. ex: byNameAndAgeComposite
        :param label: label name of vertex. ex: Person
        :param property_keys: list of property keys. ex: ['name', 'age']
        :return:
        """
        if not isinstance(property_keys, list):
            raise Exception("property_keys should be of list of property keys")
        if property_keys.__len__() == 0:
            raise Exception("property_keys should be of list type and should have "
                            "at-least one property key.")
        query_string = """
graph.tx().rollback() //Never create new indexes while a transaction is active
mgmt = graph.openManagement()"""
        add_keys_data = ""

        for property_key in property_keys:
            query_string += """
{property_key} = mgmt.getPropertyKey('{property_key}')""".format(property_key=property_key)
            add_keys_data += ".addKey({property_key})".format(property_key=property_key)

            if label:
                query_string += """
{label} = mgmt.getVertexLabel('{label}')""".format(label=label)
                add_keys_data += ".indexOnly({label})".format(label=label)

        query_string += """        
mgmt.buildIndex('{index_name}', Vertex.class).{add_keys_data}.buildCompositeIndex()        
mgmt.commit()

//Wait for the index to become available
ManagementSystem.awaitGraphIndexStatus(graph, '{index_name}').call()
""".format(index_name=index_name, add_keys_data=add_keys_data.lstrip("."))
        query_string += self.create_reindex_query(index_name)
        print(query_string)
        return self.gremlin_client.query(query_string, serialize_elements=False)

    def reindex(self, index_name):
        query_string = self.create_reindex_query(index_name)
        return self.gremlin_client.query(query_string, serialize_elements=False)


class GraphIndexOperations(CRUDOperationsBase):

    def __init__(self, gremlin_client=None):
        super(GraphIndexOperations, self).__init__(gremlin_client=gremlin_client)
        self.composite_index = CompositeIndexOperations(gremlin_client)

    #
    # def get_edge_stats(self, label):
    #     result = self.gremlin_client.query("g.E().hasLabel('{}').count()".format(label))
    #     return result[0]
