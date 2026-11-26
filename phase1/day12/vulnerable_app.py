import socket
import ipaddress
from urllib.parse import urlparse
import requests
from flask import Flask, request

app = Flask(__name__)

def is_safe_url(url):
    # 1. parse the URL and get the hostname
    hostname = urlparse(url).hostname
    if not hostname:
        return False

    # 2. resolve the hostname to an IP (this defeats the DNS trick)
    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        return False

    print(f"ip: {ip}")

    # 3. reject the request if that IP is internal
    ip_obj = ipaddress.ip_address(ip)
    print(f"ip_obj: {ip_obj}")
    if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
        print(f"BLOCKED SSRF: {url} resolves to internal IP {ip}")
        return False

    return True


@app.route("/")
def home():
    return """
    <h2>URL Preview Tool</h2>
    <form method="POST" action="/fetch">
      <input name="url" placeholder="https://example.com" style="width:400px">
      <button>Fetch</button>
    </form>
    """

@app.route("/fetch", methods=["POST"])
def fetch():
    url = request.form.get("url")

    if not is_safe_url(url):
        return "Blocked: that URL is not allowed.", 403

    print("Server is fetching:", url)
    try:
        r = requests.get(url, timeout=5)
        return f"<h3>Fetched {url}</h3><pre>{r.text[:1000]}</pre>"
    except Exception as e:
        return f"Error fetching: {e}"

if __name__ == "__main__":
    app.run(port=5000, debug=True)