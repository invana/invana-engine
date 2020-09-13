from gremlin_python.structure.graph import Vertex, Edge


class GremlinResponseSerializer:

    @staticmethod
    def serialize_vertex_dict(vtx):
        cleaned_data = {"properties": {}}
        for k, v in vtx.items():
            if str(k) == "T.id":
                cleaned_data['id'] = v.get('@value').strip("#") if type(v) is dict else v
            elif str(k) == "T.label":
                cleaned_data['label'] = v
            else:
                cleaned_data['properties'][k] = v[0]  # TODO - fix this.
        return cleaned_data

    @staticmethod
    def serialize_edge_dict(edg):
        cleaned_data = {"properties": {}}

        for k, v in edg.items():
            if str(k) == "T.id":
                cleaned_data['id'] = v.get('@value', {}).get("relationId") if type(v) is dict else v
            elif str(k) == "T.label":
                cleaned_data['label'] = v
            else:
                cleaned_data['properties'][k] = v  # TODO - fix this.
        return cleaned_data

    @staticmethod
    def serialize_vertex_element(vertex):
        return {
            "id": vertex.id,
            "label": vertex.label,
            "type": "vertex",
            "properties": None
        }

    @staticmethod
    def serialize_edge_element(edge):
        return {
            "id": edge.id,
            "label": edge.label,
            "type": "edge",
            "properties": None
        }

    def serialize_data(self, data):
        print("===", type(data))
        if isinstance(data, list):
            _serialized_data = []
            for datum in data:
                _ = self.serialize_data(datum)
                if type(_) is list:
                    _serialized_data.extend(_)
                elif type(_) is dict:
                    _serialized_data.append(_)
            return _serialized_data
        elif isinstance(data, dict):
            try:
                # TODO - use better logics to check if data is vertex or edge,
                # currently simple try except works.
                return self.serialize_vertex_dict(data)
            except Exception as e:
                return self.serialize_edge_dict(data)
        elif isinstance(data, Vertex):
            return self.serialize_vertex_element(data)
        elif isinstance(data, Edge):
            return self.serialize_edge_element(data)
        else:
            raise NotImplementedError("")
