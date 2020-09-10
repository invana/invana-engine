from urllib.parse import urlparse


def get_host(url):
    o = urlparse(url)
    return f"{o.scheme}://{o.netloc}"
