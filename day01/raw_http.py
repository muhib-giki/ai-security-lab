import socket

host = "example.com"
request=(
    "GET / HTTP/1.1\r\n"
    f"HOST: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

with socket.create_connection((host, 80)) as s:
    s.sendall(request.encode())

    response = b""

    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response += chunk

print(response.decode(errors="replace")[:1200])