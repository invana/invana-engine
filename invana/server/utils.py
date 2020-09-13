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
