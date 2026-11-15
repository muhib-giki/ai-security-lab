import requests

URLS = ["https://github.com", "https://www.google.com"]

for url in URLS:
    r = requests.get(url, timeout=10)
    print(url)
    for line in r.raw.headers.getlist("Set-Cookie"):
        print(" ", line[:150])
    print()