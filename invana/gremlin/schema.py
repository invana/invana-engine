from .base import GremlinOperationBase, CRUDOperationsBase
from gremlin_python.process.strategies import *
from gremlin_python.process.traversal import Order


class SchemaOps(GremlinOperationBase):

    def get_all_vertices_schema(self):
        _ = self.gremlin_client.execute_query(
            "g.V().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )
        schema_data = []
        for schema in _:
            for k, v in schema.items():
                schema_data.append(
                    {
                        "label": k,
                        "propertyKeys": v
                    }
                )
        return schema_data

    def get_vertex_label_schema(self, label: str, namespace: str = None):
        # TODO - fix performance
        _ = self.gremlin_client.execute_query(
            "g.V().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )
        return {"label": label, "propertyKeys": _[0].get(label, [])}

    def get_all_edges_schema(self):
        _ = self.gremlin_client.execute_query(
            "g.E().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )
        schema_data = []
        for schema in _:
            for k, v in schema.items():
                schema_data.append(
                    {
                        "label": k,
                        "propertyKeys": v
                    }
                )
        return schema_data

    def get_edge_label_schema(self, label: str, namespace: str = None):
        # TODO - fix performance
        _ = self.gremlin_client.execute_query(
            "g.E().group().by(label).by(properties().label().dedup().fold())",
            serialize_elements=False
        )
        return {"label": label, "propertyKeys": _[0].get(label, [])}

    def create_vertex_label_schema(self, label: str, namespace: str = None):

        try:
            _ = self.gremlin_client.execute_query(
                f"""
    mgmt = graph.openManagement()
    person = mgmt.makeVertexLabel('{label}').make()
    mgmt.commit()
                
                """,
                # "person = graph.addVertex(label, '" + label + "')",
                serialize_elements=False
            )
            return {"status": True, "message": "ok"}
        except Exception as e:
            return {"status": False, "message": e.__str__()}

    def create_edge_label_schema(self, label: str, multiplicity: str = None, namespace: str = None):
        # https://docs.janusgraph.org/basics/schema/#edge-label-multiplicity

        query = f"""
mgmt = graph.openManagement()
person = mgmt.makeEdgeLabel('{label}')"""
        if multiplicity:
            query += f".cardinality(Cardinality.{multiplicity.upper()})"
        query += ".make()"
        query += f"""
mgmt.commit()
        """
        try:
            _ = self.gremlin_client.execute_query(
                query,
                serialize_elements=False
            )
            return {"status": True, "message": "ok"}
        except Exception as e:
            return {"status": False, "message": e.__str__()}

    def create_vertex_property_schema(self,
                                      label: str,
                                      property_key: str,
                                      data_type: str,
                                      cardinality: str):
        """

        :param label:
        :param property_key:
        :param data_type:
        :param cardinality: SINGLE, LIST , SET
        :return:
        """

        query = f"""
        mgmt = graph.openManagement()
        {property_key}_prop = mgmt.makePropertyKey('{property_key}')
        """
        if data_type:
            query += f".dataType({data_type}.class)"
        if cardinality:
            query += f".cardinality(Cardinality.{cardinality.upper()})"
        query += ".make()"
        query += f"""
        
        {label}_label = mgmt.getVertexLabel("{label}")        
        mgmt.addProperties({label}_label, {property_key}_prop)
        mgmt.commit()
        """

        print("====", query)
        try:
            _ = self.gremlin_client.execute_query(
                query,
                serialize_elements=False
            )
            print("====", _)
            return {"status": True, "message": "ok"}
        except Exception as e:
            return {"status": False, "message": e.__str__()}

    def create_edge_property_schema(self,
                                    label: str,
                                    property_key: str,
                                    data_type: str,
                                    cardinality: str):
        """

        :param label:
        :param property_key:
        :param data_type:
        :param cardinality: SINGLE, LIST , SET
        :return:
        """

        query = f"""
        mgmt = graph.openManagement()
        {property_key}_prop = mgmt.makePropertyKey('{property_key}')
        """
        if data_type:
            query += f".dataType({data_type}.class)"
        if cardinality:
            query += f".cardinality(Cardinality.{cardinality.upper()})"
        query += ".make()"
        query += f"""
        
        {label}_label = mgmt.getEdgeLabel("{label}")        
        mgmt.addProperties({label}_label, {property_key}_prop)
        mgmt.commit()
        """
        try:
            _ = self.gremlin_client.execute_query(
                query,
                serialize_elements=False
            )
            print("====", _)
            return {"status": True, "message": "ok"}
        except Exception as e:
            return {"status": False, "message": e.__str__()}
