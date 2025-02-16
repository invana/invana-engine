from invana_engine.types import RelationShip, Node, \
    Property, VertexProperty, GenericData
import logging

logger = logging.getLogger(__name__)


class CypherSerializer:
    # https://community.neo4j.com/t/convert-stream-of-records-to-json-in-python-driver/39720/3


    def serialize_data_custom(self, index, record):
        """
        A custom serializer.

        Keyword arguments:
        index -- optional
        record -- required

        Record class documentation - https://neo4j.com/docs/api/python-driver/4.2/api.html#record
        """
        # Create an empty dictionary
        graph_data_type_list = {}
        # Iterate over the list of records also enumerating it.
        for j, graph_data_type in enumerate(record):
            # Check if the record has string or integer literal.
            if isinstance(graph_data_type, str) or isinstance(graph_data_type, int):
                # Return the keys and values of this record as a dictionary and store it inside graph_data_type_dict.
                graph_data_type_dict = record.data(j)
            else:

                # If the record fails the above check then manually convert them into dictionary with __dict__
                graph_data_type_dict = graph_data_type.__dict__
                # Remove unnecessary _graph as we do not need it to serialize from the record.
                if '_graph' in graph_data_type_dict:
                    del graph_data_type_dict['_graph']
                # Add a _start_node key from the record.
                if '_start_node' in graph_data_type_dict:
                    graph_data_type_dict['_start_node'] = graph_data_type_dict['_start_node'].__dict__
                    # Add a _labels key of start node from the record.
                    if '_labels' in graph_data_type_dict['_start_node']:
                        frozen_label_set = graph_data_type.start_node['_labels']
                        graph_data_type_dict['_start_node']['_labels'] = [v for v in frozen_label_set]
                    # Remove unnecessary _graph as we do not need it to serialize from the record.
                    if '_graph' in graph_data_type_dict['_start_node']:
                        del graph_data_type_dict['_start_node']['_graph']
                # Add a _start_node key from the record.
                if '_end_node' in graph_data_type_dict:
                    graph_data_type_dict['_end_node'] = graph_data_type_dict['_end_node'].__dict__
                    # Add a _labels key of start node from the record.
                    if '_labels' in graph_data_type_dict['_end_node']:
                        frozen_label_set = graph_data_type.start_node['_labels']
                        graph_data_type_dict['_end_node']['_labels'] = [v for v in frozen_label_set]
                    # Remove unnecessary _graph as we do not need it to serialize from the record.
                    if '_graph' in graph_data_type_dict['_end_node']:
                        del graph_data_type_dict['_end_node']['_graph']
                # Add other labels for representation from frozenset()
                if '_labels' in graph_data_type_dict:
                    frozen_label_set = graph_data_type_dict['_labels']
                    graph_data_type_dict['_labels'] = [v for v in frozen_label_set]

                if hasattr(graph_data_type, "type") and '_labels' in graph_data_type_dict \
                      and  graph_data_type_dict['_labels'].__len__() == 0:
                    graph_data_type_dict['_labels'] = [graph_data_type.type]
                # print(graph_data_type_dict) # test statement
            graph_data_type_list.update(graph_data_type_dict)
        return graph_data_type_list
    

    def create_vertex_object(self, node):
        try:
            properties = []
            for key, value in node['_properties'].items():
                properties.append(VertexProperty(key=key, value=value))
            return Node(id=node['_id'], label=node['_labels'][0], properties=properties)
        except Exception as e :
            logger.debug(f"Failed to create Node object with error : {e.__str__()}")
            return node

    def create_edge_object(self, edge):
        try:
            properties = []
            for key, value in edge['_properties'].items():
                properties.append(Property(key=key, value=value))
            return RelationShip(id=edge['_id'], label=edge['_labels'][0],
                            outV=self.create_vertex_object(edge['_start_node']) ,
                            inV=self.create_vertex_object(edge['_end_node']) ,
                            properties=properties)
        except Exception as e :
            logger.debug(f"Failed to create Relationship object with error : {e.__str__()}")
            return edge
        

    def convert_to_invana_objects(self, result_json):
        result_objs = []
        for r in result_json:
            if type(r) is dict:
                if  r.get("_element_id") and r.get("_start_node"): 
                    # relationship
                    result_objs.append(self.create_edge_object(r))
                elif r.get("_element_id"):
                    # node
                    result_objs.append(self.create_vertex_object(r)) # TODO - assign Node, Relationship
                else:
                    result_objs.append(GenericData(r))
            else:
                result_objs.append(GenericData(r))
        return result_objs
        
    
    def serialize_response(self, result):
        _ =   [self.serialize_data_custom(index, record) for index, record in enumerate(result)]
        _ = self.convert_to_invana_objects(_)
        return _
