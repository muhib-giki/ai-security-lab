import socket
import ssl
from pprint import pprint

import certifi

host = "github.com"
context = ssl.create_default_context(cafile=certifi.where())

with socket.create_connection((host, 443), timeout=10) as sock:
    with context.wrap_socket(sock, server_hostname=host) as ssock:
        cert = ssock.getpeercert()

pprint(cert)