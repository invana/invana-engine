from importlib import import_module


def import_klass(klass_path_string):
    components = klass_path_string.split('.')
    module = import_module(".".join(components[0: (components.__len__() - 1)]))
    return getattr(module, components[-1])


def get_unique_items(elements):
    vertices = []
    edges = []
    existing_vertices = []
    existing_edges = []

    for elem in elements:
        elem_type = elem.type
        if elem_type == "g:Edge" and elem.id not in existing_edges:
            existing_edges.append(elem.id)
            edges.append(elem)
        elif elem_type == "g:Vertex" and elem.id not in existing_vertices:
            existing_vertices.append(elem.id)
            vertices.append(elem)
    return vertices + edges
