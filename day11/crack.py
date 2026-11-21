import hashlib

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

# stolen from the database — three users' password hashes
stolen = {
    "muhib": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
    "alice": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
    "admin": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
}

# attacker's wordlist of common passwords to try
wordlist = ["123456", "password", "password123", "qwerty", "letmein", "admin", "welcome"]

# precompute the hash of every word, then look for matches
lookup = {sha256(word): word for word in wordlist}


for user, hashed in stolen.items():
    if hashed in lookup:
        print(f"CRACKED {user}: {lookup[hashed]}")
    else:
        print(f"{user}: not in wordlist")