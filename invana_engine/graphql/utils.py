from urllib.parse import urlparse
import socket


def get_host(url):
    o = urlparse(url)
    return f"{o.scheme}://{o.netloc}"


def get_client_info():
    # get the info of the server where this graphql is running.
    hostname = socket.gethostname()
    # _ = socket.gethostbyaddr()
    return {
        'host_name': hostname,
        'host_ip_address': socket.gethostbyname(hostname),
        "host_port": 1
    }
