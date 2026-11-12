import socket
import ssl
import certifi

host = "wrong.host.badssl.com"
request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

context = ssl.create_default_context(cafile=certifi.where())

with socket.create_connection((host, 443), timeout=10) as sock:
    with context.wrap_socket(sock, server_hostname=host) as ssock:
        print("TLS version:", ssock.version())
        print("Cipher:", ssock.cipher())

        ssock.sendall(request.encode())

        response = b""
        while True:
            chunk = ssock.recv(4096)
            if not chunk:
                break
            response += chunk

print(response.decode(errors="replace")[:1200])