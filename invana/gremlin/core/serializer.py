from gremlin_python.structure.graph import Vertex, Edge


class GremlinResponseSerializer:

    def get_element_id(self, _id):
        if type(_id) is dict:
            _id = _id["@value"]
        if type(_id) is dict:
            _id = _id['relationId']
        if type(_id) is str:
            _id = _id.strip("#")
        return _id

    def serialize_element_dict(self, elem):
        cleaned_data = {"properties": {}}
        if "Direction.IN" in elem.keys():
            cleaned_data['type'] = "edge"
        else:
            cleaned_data['type'] = "vertex"
        for k, v in elem.items():
            if str(k) == "T.id":
                cleaned_data['id'] = self.get_element_id(v)
            elif str(k) == "T.label":
                cleaned_data['label'] = v
            elif str(k) == "Direction.OUT":
                _ = self.serialize_element_dict(v)
                cleaned_data.update({"outV": _['id'], "outVLabel": _['label']})
            elif str(k) == "Direction.IN":
                _ = self.serialize_element_dict(v)
                cleaned_data.update({"inV": _['id'], "inVLabel": _['label']})
            else:
                # TODO - check if this is right.
                cleaned_data['properties'][k] = v[0] if type(v) is list else v
        if cleaned_data['properties'].keys().__len__() == 0:
            del cleaned_data['properties']

        return cleaned_data

    def serialize_vertex_element(self, vertex):
        return {
            "id": vertex.id,
            "label": vertex.label,
            "type": "vertex",
            "properties": {}
        }

    def serialize_edge_element(self, edge):
        return {
            "id": edge.id,
            "label": edge.label,
            "type": "edge",
            "inV": edge.inV.id,
            "inVLabel": edge.inV.label,
            "outV": edge.outV.id,
            "outVLabel": edge.outV.label,
            "properties": {}
        }

    def serialize_data(self, data):
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
            return self.serialize_element_dict(data)
        elif isinstance(data, Vertex):
            return self.serialize_vertex_element(data)
        elif isinstance(data, Edge):
            return self.serialize_edge_element(data)
        else:
            raise NotImplementedError("")
