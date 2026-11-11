import requests

# r = requests.get("https://example.com", timeout=10)
r = requests.get("http://github.com", timeout=10)

print("Status:", r.status_code)
print("Final URL:", r.url)
print("History:", r.history)

print("--- Request Headers ---")
for name, value in r.request.headers.items():
    print(f"{name}: {value}")

print("--- Response Headers ---")
for name, value in r.headers.items():
    print(f"{name}: {value}")

print("--- Redirect history ---")
for old in r.history:
    print(old.status_code, old.url)