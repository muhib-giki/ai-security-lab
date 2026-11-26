# Security Reference Sheet — Days 1–14
*Keep this open while working. Do NOT memorize it. Glance at it; the common ones stick on their own over time.*

---

## The ONE idea behind half the attacks
**Never let untrusted data become code.** Keep data and code separate.
- HTML context → **escape** output (`&lt;` etc.)
- SQL context → **parameterized queries** (`?` placeholders)
- OS command context → **argument list**, no shell

## The OTHER recurring ideas
- **Never trust the client** — UI/URL/hidden fields/cookies are all attacker-controlled. Re-check on the server.
- **Allowlist, don't blocklist** — name what's allowed, deny the rest. (CSP, open redirect, SSRF, SQL.)
- **Defense in depth** — layers; one failing doesn't break everything.
- **Keep secrets useless after a breach** — hash passwords (bcrypt).

---

## Security headers — which does what
| Header | Purpose (what it stops) | Strong value |
|---|---|---|
| `Strict-Transport-Security` (HSTS) | forces HTTPS → stops SSL-strip / MITM | `max-age` ≥ ~6mo (15768000+) |
| `Content-Security-Policy` (CSP) | controls what scripts can run → stops **XSS** | no `'unsafe-inline'`, no `*` |
| `X-Frame-Options` | stops your site being framed → **clickjacking** | `DENY` or `SAMEORIGIN` |
| `X-Content-Type-Options` | stops MIME-sniffing | `nosniff` |
| `Referrer-Policy` | limits URL leakage to other sites | set (not `unsafe-url`) |
*Present ≠ good. Check the VALUE. Your scanner does this for you.*

## Cookie flags — which does what
| Flag | Purpose | 
|---|---|
| `Secure` | only sent over HTTPS (stops network reading) |
| `HttpOnly` | JS can't read it (stops **XSS** cookie theft) |
| `SameSite=Lax/Strict` | not sent on cross-site requests (stops **CSRF**) |
*Session cookie should have all three. A theme cookie needn't.*

---

## The attacks — recognize + fix
| Attack | One-line tell | Fix |
|---|---|---|
| **Clickjacking** | site loads in an `<iframe>` | `X-Frame-Options: DENY` / CSP `frame-ancestors` |
| **CSRF** | action decided by cookie alone, no proof it came from your page | `SameSite` + **CSRF token** (secret in your own form) |
| **XSS** | user input shown on a page unescaped → `<script>` runs | **escape output** + CSP; cookie `HttpOnly` |
| **SQL injection** | input concatenated into a query → `' OR '1'='1' --` | **parameterized queries** (`?`) |
| **Broken access control / IDOR** | change `/note/1`→`/note/2`, see others' data | check **ownership** + **role** on every request, server-side |
| **Auth / passwords** | plaintext passwords; unlimited login attempts | **bcrypt** hashing + **rate limit / lockout** |
| **SSRF** | server fetches a user-supplied URL (image-from-URL, webhook, preview) | **allowlist** + resolve host, block internal IPs (`127.*`,`10.*`,`192.168.*`,`169.254.*`) |
| **Command injection** | user input in an OS command via shell → `; whoami` | **arg list**, `shell=False`; avoid shelling out; validate |
| **Misconfiguration** | debug on, default creds, verbose errors, missing headers | turn off debug, generic errors, deployment checklist |

## Session-attack trio (no password needed)
- **Hijacking** = steal the session ID value.   
- **Clickjacking** = steal a click (site stays logged in inside a frame).
- **CSRF** = borrow the browser's auto-sent cookie.
- **XSS defeats all defenses** — runs inside your page as first-party code (reads cookies/tokens, forges requests).

---

## Code patterns I'll always look up (that's fine)
```python
# escape (XSS)        from markupsafe import escape ;  escape(user_input)
# SQL placeholder     db.execute("... WHERE id = ?", (note_id,))      # 1-item tuple needs comma!
# command, safe       subprocess.run(["ping","-n","2",host], shell=False)
# password hash       bcrypt.hashpw(pw.encode(), bcrypt.gensalt()) ; bcrypt.checkpw(pw.encode(), stored)
# session cookie      resp.set_cookie("session_id", sid, httponly=True, samesite="Lax")  # +secure on HTTPS
# SSRF IP check       ipaddress.ip_address(ip).is_private / .is_loopback / .is_link_local
```

## Debug-by-layer (when a request fails)
DNS (`gaierror`) → TCP (`TimeoutError`/refused) → TLS (`SSLError`) → HTTP (status codes).

---
*The job is recognition + explanation, not recall. If you can say "this is X, fixed by Y," the exact syntax is a lookup.*