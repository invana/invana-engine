from urllib.parse import urlparse
import socket


def get_host(url):
    o = urlparse(url)
    return f"{o.scheme}://{o.netloc}"


def get_client_info():
    hostname = socket.gethostname()
    return {
        'host_name': hostname,
        'ip_address': socket.gethostbyname(hostname)
    }


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


