import requests

URL = "https://httpbin.org/post"

# payload = {"username": "muhib", "plan": "free"}
payload = {"username": "muhib", "plan": "premium", "is_admin": True}

form = requests.post(URL, data=payload, timeout=10)

print("--- form ---")
print("content-type header sent: ", form.request.headers["Content-Type"])
print("body sent: ", form.request.body)
print("server received: ", form.json()["form"])

js = requests.post(URL, json=payload, timeout=10)

print("--- json ---")
print("content-type header sent: ", js.request.headers["Content-Type"])
print("body sent: ", js.request.body)
print("server received: ", js.json()["json"])