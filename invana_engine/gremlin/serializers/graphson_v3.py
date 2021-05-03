import logging

from gremlin_python.structure.graph import Vertex, Edge, Path


class GraphSONV3Reader:

    @staticmethod
    def get_element_id(_id):
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
            cleaned_data['type'] = "g:Edge"
        else:
            cleaned_data['type'] = "g:Vertex"
        for k, v in elem.items():
            if str(k) == "T.id":
                if self.get_element_id(v):
                    cleaned_data['id'] = self.get_element_id(v)
                else:
                    raise Exception("This element doesnt have id, ( may be path)")

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
                if type(v) is list:
                    if v.__len__() > 0:
                        if not isinstance(v[0], Edge) or not isinstance(v[0], Vertex):
                            cleaned_data['properties'][k] = v[0]
                        else:
                            raise Exception("This element is not a element dictionary, ( may be path)")
                elif isinstance(v, Edge):
                    raise Exception("This element is not a element dictionary, Edge found in iter, ( may be path)")
                elif isinstance(v, Vertex):
                    raise Exception("This element is not a element dictionary Vertex found in iter, ( may be path)")
                else:
                    cleaned_data['properties'][k] = v

        if cleaned_data['properties'].keys().__len__() == 0:
            del cleaned_data['properties']
        return cleaned_data

    @staticmethod
    def serialize_vertex_element(vertex):
        print("=====vertex", vertex)
        return {
            "id": vertex.id,
            "label": vertex.label,
            "type": "g:Vertex",
            "properties": {}
        }

    def serialize_edge_element(self, edge):

        _ = {
            "id": self.get_element_id(edge.id),
            "label": edge.label,
            "type": "g:Edge",
            "in_v": edge.inV.id,
            "in_v_label": edge.inV.label,
            "out_v": edge.outV.id,
            "out_v_label": edge.outV.label,
            "properties": {}
        }
        return _

    def serialize_data(self, data):
        if isinstance(data, list):
            _serialized_data = []
            for datum in data:
                _ = self.serialize_data(datum)
                if type(_) is list:
                    _serialized_data.extend(_)
                else:
                    _serialized_data.append(_)
            return _serialized_data

        elif isinstance(data, dict):
            keys = list(data.keys())
            if "label" in keys and "type" in keys:
                # TODO - find a better way to distinguish already invana serialised element.
                return data
            else:
                try:
                    return self.serialize_element_dict(data)
                except Exception as e:
                    logging.debug(e)
                    _serialised_data = []
                    for key, val in data.items():
                        if type(val) is list:
                            _serialised_data.extend(self.serialize_data(val))
                        else:
                            _serialised_data.append(self.serialize_data(val))
                    return _serialised_data
        elif isinstance(data, Vertex):
            return self.serialize_vertex_element(data)
        elif isinstance(data, Edge):
            return self.serialize_edge_element(data)
        elif isinstance(data, Path):
            _serialized_data = []
            for datum in data:
                _ = self.serialize_data(datum)
                _serialized_data.append(_)
            return _serialized_data
        else:
            raise NotImplementedError("")
