# Day 7 — CSRF (Cross-Site Request Forgery)

## The core idea
- The browser attaches a site's cookie to **every** request to that site, no matter which page started it.
- **CSRF:** an attacker's page sends a request to a site you're logged in to; the browser attaches your cookie; the server performs the action.
- The attacker never sees or steals the cookie. **CSRF is not cookie leakage** — it abuses the cookie being auto-sent.
- Works only when the server decides on the **cookie alone** (no proof the request came from its own page).

## Three session attacks compared (not all cookie theft)
| Attack | Abuses | Attacker gets the cookie value? |
|---|---|---|
| Session hijacking | a stolen session ID | Yes |
| Clickjacking | your click on your logged-in site | No |
| CSRF | the browser auto-sending the cookie | No |

## The attack (built)
- Attacker page auto-submits a hidden form to the victim's POST route:
```html
<form id="evil" method="POST" action="http://127.0.0.1:5000/change-email">
  <input name="email" value="attacker@evil.com">
</form>
<script>document.getElementById("evil").submit();</script>
```
- Target was a **change-email** feature — real-world first step of account takeover (change email → password reset to attacker).

## SameSite — what I actually observed
- `SameSite` decides "same site" by **hostname + TLD, ignoring the port**.
  - victim `127.0.0.1:5000` + attacker `127.0.0.1:8000` = **same site** → cookie sent → attack worked.
  - attacker on `localhost:8000` vs victim `127.0.0.1` = **different site** → cookie withheld → blocked.
- `localhost` and `127.0.0.1` are different hostnames.
- `Lax`: withholds cookie on cross-site **POST**, allows it on cross-site top-level **GET** (link clicks). Has grace windows → not reliable.
- `Strict`: withholds on all cross-site requests, incl. link clicks → user looks logged out after following a link (usability cost).
- For a cross-site **POST**, Lax and Strict both block — they only differ on GET. Another reason data-changing actions must never be GET.
- **SameSite is a first layer, not a guarantee** (depends on browser, timing, method, same-site definition).

## Fix 2 — CSRF token (the real fix)
- Server plants a secret random value in its **own** form (hidden field), stored per session.
- Real submit sends it back; attacker's page can't know it (can't read cross-site page content).
- Server rejects (403) any request without the matching token.
```python
token = secrets.token_hex(16)
CSRF_TOKENS[session_id] = token
# <input type="hidden" name="csrf_token" value="{token}">
if not sent_token or sent_token != real_token:
    return "CSRF check failed", 403
```
- Blocks the attack regardless of hostname, port, browser, GET/POST, or SameSite. Proved it in the same-site setup where SameSite was useless.
- Use **both**: SameSite (cheap first layer) + token (the one you trust) = defense in depth.

## In a real system
- **CSRF only works when the browser auto-attaches the credential → cookie auth.**
- Auth via `Authorization: Bearer <token>` header (APIs, SPAs, mobile): browser does NOT auto-add it → not CSRF-prone.
- Trade-off (classic interview Q):
  - Cookie (auto-sent): CSRF-exposed, but `HttpOnly` protects it from XSS theft.
  - Token in localStorage (read by JS): CSRF-safe, but XSS can read it.
  - No free option.

## In my own words
-
-
-