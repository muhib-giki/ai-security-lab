# Day 11 — Authentication Done Properly

## The problem with plaintext passwords
- DB leaks happen (SQLi, backups). If passwords are plaintext → instant total compromise, made worse by password reuse across sites.
- Goal isn't only "stop the leak" (can't fully). It's "make a stolen password table **useless**."
- **Never store the password.** Store something you can check against but can't reverse.

## Hashing
- Hash function: any input → fixed-length output. **Deterministic** (same in → same out) and **one-way** (can't reverse).
- Store the hash; at login, hash the input and compare hashes. Password itself is never stored.

## Why plain hashing (SHA-256) is NOT enough
1. **One-way ≠ secret.** Attacker hashes a wordlist forward and matches. Common passwords crack instantly via precomputed tables.
2. **Identical passwords → identical hashes.** Attacker sees two matching hashes = same password, cracks both at once; one table cracks every DB worldwide.

### Salt — fixes #2
- Random value added per-password before hashing: `hash(salt + password)`.
- Different salt per user → same password gives different hashes → precomputed tables useless.
- Salt is **not secret** (stored next to the hash). Its job is uniqueness, not secrecy.

## Why even salted SHA-256 is still wrong for passwords
- SHA-256 is **fast** (billions/sec). Salt stops precomputed tables but each guess is still cheap → weak passwords fall in seconds.
- Need a **deliberately slow** password hash: **bcrypt / scrypt / argon2**.
  - Slow by design, tunable (cost factor), to stay ahead of faster hardware.
  - Salt built in (auto, per password).
  - Algorithm + salt + hash bundled in one output string.
- **Rule: SHA-256/MD5 = data integrity. Passwords = bcrypt/argon2.** Mixing them up is a real audit finding.

## bcrypt
```python
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())   # on signup
ok = bcrypt.checkpw(entered.encode(), hashed)                 # on login -> True/False
```
- Output: `$2b$12$<22-char salt><31-char hash>` → `2b`=bcrypt, `12`=cost factor (2^12 rounds), then salt+hash.
- `checkpw` reads the salt out of the stored string — no separate salt column.
- Confirmed in my output: two users with the same password had **different** hashes (auto salt).

## Second front door: brute-force at the live login
- Hashing protects the **stolen DB**. It does NOTHING against guessing passwords at the real login page.
- Attack: POST the login repeatedly with a password list until one returns success.

### Fix — rate limiting / lockout
```python
if FAILED_ATTEMPTS.get(username, 0) >= MAX_ATTEMPTS:
    return "Too many failed attempts", 429     # refuse BEFORE checking password
# wrong password -> FAILED_ATTEMPTS[username] += 1
# correct password -> reset to 0
```
- `429 Too Many Requests` = standard rate-limit status.
- Two fronts covered: **hashing** (stolen data) + **rate limiting** (live login).

### Limits of the simple version (interview points)
- No time window → locks forever. Real: attempts-per-minute (Flask-Limiter).
- Lock-by-username lets an attacker **lock you out** (DoS) → rate-limit by **IP** or use CAPTCHA.
- In-memory counter resets on restart, doesn't span servers → use Redis.

## In my own words
-
-
-