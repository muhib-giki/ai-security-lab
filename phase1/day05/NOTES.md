# Day 5 — The server side: login and sessions

## A server is a program that waits for requests
- `127.0.0.1` / `localhost` = this same computer. Port (5000) picks the program.
- **Route:** which function answers which path.
- What the function returns becomes the response body.
- The server only sees text the client sent (User-Agent, cookies, form fields). It can't verify any of it by looking.
- The server log records every request line, including query strings.
- A new site has **no** security headers or cookie settings. The developer has to add them.

## Why login needs sessions
- Checking a password once isn't enough: the next request arrives as a stranger.
- Without sessions, a "private" page is served to anyone (status 200).

## How a session works
1. Password correct → server makes a **random ID** (`secrets.token_hex(16)`).
2. Server saves `ID → username` in **its own table**.
3. Server sends the ID as a cookie (`Set-Cookie`).
4. On each request, server reads the cookie, looks the ID up, and decides.

- Use `secrets` for anything security-related, never `random` (predictable).
- An ID only works while the server's table contains it.

## Session hijacking (done by hand)
- A script with the copied session ID and **no password** got the private page.
- The server can't tell the real browser from any program sending the same value.
- Each cookie setting closes one way of getting that value.

## HttpOnly, seen in action
- Before: `document.cookie` in the Console showed the session ID → any script on the page could read it.
- After `httponly=True`: `document.cookie` is empty, and the site still works (the browser still sends the cookie).
- Limit: still visible in DevTools and on the network. `Secure` (HTTPS only) covers the network.

## Logout
- A login lives in two places: the **browser cookie** and the **server's row**.
- Deleting only the cookie: browser is logged out, but a copied ID still works.
- Correct logout deletes the **row** too. Audit finding name: "session not invalidated on logout".
- Logout changes something → make it a **POST**, not a GET.

## Other lessons
- Error message "Wrong username or password": never reveal which one was wrong (stops attackers learning which accounts exist).
- Never store passwords as plain text (to be fixed in Phase 1).
- `debug=True` is for development only; on a public server it lets visitors run code.
- Debug mode restarts on every saved file in the folder → memory is wiped. Real apps keep sessions in a database.

## Python / Flask
```python
app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login(): ...

request.method / request.path / request.args / request.form / request.cookies / request.headers
return "text", 401                       # body + status
response = make_response(redirect("/dashboard"))
response.set_cookie("session_id", sid, httponly=True, samesite="Lax")
response.delete_cookie("session_id")
```
- `{"a": "b"}` is a **dictionary**; `{"a", "b"}` is a **set** (no values to look up). One character apart.
- "not subscriptable" = you used `[...]` on something that doesn't support it.
- `d.pop(key, None)` removes a key without an error if it's missing.
- `"""..."""` for strings that span several lines.
- `sys.argv[1]` = first word typed after the script name.

## In my own words
-
-
-