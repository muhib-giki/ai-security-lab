# Day 10 — Broken Access Control

## The core confusion (this IS the vulnerability)
- **Authentication** = "Who are you?" (login, session) — Day 5.
- **Authorization** = "Are you allowed to do THIS specific thing?"
- Broken access control = app checks auth**entication** but forgets auth**orization**. Confirms you're logged in, then gives you whatever you ask for without checking it's yours.
- #1 on the OWASP Top 10. Most common serious bug in real apps and in bug bounty.

## IDOR (Insecure Direct Object Reference) — reading others' data
- App puts a raw ID in the URL: `/note/1`. Change to `/note/2` → someone else's data.
- App checked "logged in?" (yes) but never "is note 2 yours?".
- **Trivial to exploit:** just change/increment the number. No payload.
- **Invisible in testing:** devs test with their own data, so it always looks correct. Only breaks when someone asks for an ID that isn't theirs.
- Automated dump = a loop over IDs with one logged-in session:
```python
s = requests.Session(); s.get(".../login/muhib")
for note_id in range(1, 11):
    r = s.get(f".../note/{note_id}")
```

## Privilege escalation — doing admin actions as a normal user
- Same flaw applied to **actions**, not just reads ("vertical" escalation = moving up in permission).
- Classic trap: the **page** (`/admin`) checks the role, but the **action route** (`/delete-note`) only checks login.
- Hiding the button is not a control — the route still exists. Client controls what it sends (Day 4), so the attacker calls the route directly and skips the UI.

## The fixes
**Ownership check (IDOR):**
```python
if owner != username:
    return "Forbidden", 403
# better — bake it into the query so you can't forget:
db.execute("SELECT ... FROM notes WHERE id = ? AND owner = ?", (note_id, username))
```
**Role check (escalation) — on the ACTION route, not the page:**
```python
if username != "admin":
    return "Forbidden: admins only", 403
```
- 404 vs 403 nuance: 403 reveals "this exists, you can't see it"; 404 reveals nothing. 404 can be the safer choice.

## The principle
- **Every request enforces access control on the server:** for every object "is it the user's?"; for every action "is the user allowed?". Never trust UI, URL, or client.
- Why it's #1: unlike SQLi (one fix pattern) or XSS (escape at output), this check must be written on **every** endpoint. Miss it on one route out of hundreds → that's the hole. It's a discipline, not a single fix.

## In a real system
- IDs are often sequential/guessable (invoice 41 → 42). Using UUIDs makes guessing harder but is NOT a fix — the ownership check is the fix.
- Real breaches of millions of records are usually IDOR: a URL with a guessable number and no ownership check.

## In my own words
-
-
-