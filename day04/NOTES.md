# Day 4 — Sending data and cookies

## The request body
```
POST /login HTTP/1.1
Host: example.com
Content-Type: application/json      ← how to read the body
Content-Length: 43                  ← how many bytes it has
                                    ← blank line
{"username": "muhib", "password": "12345"}
```
| Format | Content-Type | Looks like |
|---|---|---|
| Form | `application/x-www-form-urlencoded` | `username=muhib&plan=free` |
| JSON | `application/json` | `{"username": "muhib", "plan": "free"}` |

- **Forms have no types:** everything is text. `'False'` is a non-empty string, so it counts as true.
- **JSON keeps types:** an attacker can send a list or number where text is expected.

## GET vs POST
- GET: data in the URL, for reading. POST: data in the body, for changing things.
- **POST is not "secure". Only HTTPS protects data in transit.**
- GET must never change anything (browsers, previews and crawlers load links automatically).

## The client controls everything it sends
- Frontend validation, hidden fields and disabled buttons don't exist for an attacker.
- Every check that matters must be repeated on the server.
- **Mass assignment:** server copies every incoming field into the record (`is_admin=true`). Fix: accept only a fixed list of fields.

## Cookies
```
Server → client:   Set-Cookie: session_id=abc123     "keep this and show it next time"
Client → server:   Cookie: session_id=abc123         "here's what you gave me"
```
- HTTP forgets you between requests. A cookie is a note the **server writes and the client keeps**.
- **Login:** server creates a random session ID, saves "ID → user" in its own table, sends the ID as a cookie. Later it looks the ID up.
- **Whoever sends the cookie is treated as that user** (session hijacking). No password needed.
- Session IDs must be long and random.
- The client can write any cookie it likes. Never trust values like `role=admin` from a cookie.

## Cookie settings
| Setting | Tells the browser | Protects against |
|---|---|---|
| `Secure` | Send only over HTTPS | Reading it on the network |
| `HttpOnly` | Hide it from JavaScript | A script stealing it (XSS) |
| `SameSite` | Don't send on requests started by other sites | CSRF |

- `SameSite`: `Strict` (never cross-site), `Lax` (normal link clicks only), `None` (always; needs `Secure`).
- **CSRF:** another site makes your browser send a request to a site you're logged in to; the browser attaches your cookie automatically.
- `HttpOnly` doesn't prevent XSS; it removes the best thing to steal.
- `Max-Age` / `Expires`: lifetime. `Domain=.site.com`: sent to all subdomains.
- `__Secure-` name prefix: browser only accepts it over HTTPS with `Secure`.
- Good session cookie: `Secure; HttpOnly; SameSite=Lax`.
- **Not every cookie needs every setting.** A missing setting matters only on a cookie that proves a login. The tool reports; you judge.

## Python
```python
requests.post(url, data={...})        # form body
requests.post(url, json={...})        # JSON body
r.json()                              # JSON response → dict
r.request.headers / r.request.body    # what was actually sent

s = requests.Session()                # remembers cookies like a browser
requests.get(url, cookies={...})      # send a cookie typed by hand
r.raw.headers.getlist("Set-Cookie")   # one item per cookie
```
- Plain `requests.get()` can receive or send a cookie but remembers nothing. Use a `Session` for anything involving login.
- `"a; b".split(";")` → list. `.split("=", 1)` cuts once only.
- `parts[1:]` → everything after the first item.
- `.lower()` for case-insensitive comparison. `.startswith("x")`.
- `flag = "secure" in flags` stores True/False.
- `{name:20}` or `{name:<20}` pads to 20 characters, left-aligned.
- Show names and settings in output, not long secret values.

## In my own words
-
-
-