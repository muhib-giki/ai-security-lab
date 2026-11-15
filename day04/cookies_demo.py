import requests

BASE = "https://httpbin.org"

print("--- 1. without a session ---")

requests.get(f"{BASE}/cookies/set?session_id=abc_123", timeout=10)
r = requests.get(f"{BASE}/cookies", timeout=10)
print("Server sees:", r.json()["cookies"])

print("--- 2. with a session ---")
s = requests.Session()
s.get(f"{BASE}/cookies/set?session_id=abc_123", timeout=10)
r = s.get(f"{BASE}/cookies", timeout=10)
print("Server sees:", r.json()["cookies"])
print("Cookie header sent:", r.request.headers.get("Cookie"))

print("--- 3. the raw Set-Cookie header ---")
r = requests.get(f"{BASE}/cookies/set?session_id=abc123", timeout=10, allow_redirects=False)
print("Status:", r.status_code)
print("Set-Cookie:", r.headers.get("Set-Cookie"))

print("--- 4. a cookie typed by hand ---")
r = requests.get(f"{BASE}/cookies", cookies={"session_id": "someone-elses-id", "role": "admin"}, timeout=10)
print("Server sees:", r.json()["cookies"])
