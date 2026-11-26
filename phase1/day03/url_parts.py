from urllib.parse import urlparse, parse_qs

urls = [
    "https://shop.example.com:8443/products/view?id=42&sort=asc#reviews",
    "https://mybank.com@evil.com/login",
    "//evil.com/path",
    "example.com/login",
    "https://EXAMPLE.com/Admin",
    "https://site.com/search?q=apple&q=banana",
]

for url in urls:
    parts = urlparse(url)
    print(url)
    print("scheme: ", parts.scheme)
    print("username: ", parts.username)
    print("hostname: ", parts.hostname)
    print("port: ", parts.port)
    print("path: ", parts.path)
    print("query: ", parse_qs(parts.query))
    print("fragment: ", parts.fragment)
    print()