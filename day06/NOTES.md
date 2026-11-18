# Day 6 — Clickjacking (X-Frame-Options)

## What it is
- An `<iframe>` loads one web page inside another (YouTube embeds, Stripe box, maps).
- A framed site **still gets its cookies**, so a logged-in site stays logged in inside the frame.
- **Clickjacking:** attacker puts your logged-in site in an **invisible** frame (opacity 0) and floats a tempting button underneath. Your click lands on a button inside your site, as a real action.

## The three ingredients
1. Your site can be framed.
2. The frame is logged in (cookie rides along).
3. The frame is invisible and lined up over bait.

## Real example
- Twitter "Don't Click" worm: invisible Tweet button over a "Don't Click" button → victims tweeted the trap, spreading it.
- Also hits router admin pages, account settings, one-click actions.
- **Limit:** attacker steals only **clicks**, can't read data or type into the frame (cross-origin read is blocked). So it only works on actions that need a click or two.

## The fix — tell the browser not to allow framing
```python
@app.after_request
def set_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'none'"
    return response
```
- `X-Frame-Options: DENY` (old, all browsers) — or `SAMEORIGIN` to allow own site only.
- `CSP: frame-ancestors 'none'` (modern replacement). Sites send both.
- `@app.after_request` runs after every response → set security headers in one place so no route is forgotten.
- After the fix: the frame loads empty/error, bait has nothing behind it, site works normally when visited directly.

## SameSite lessons (seen early, by accident)
- `127.0.0.1` and `localhost` are **different hostnames** to the browser → cookie set on one isn't sent to the other.
- `SameSite=Lax` withholds the cookie on cross-site framed requests. A `file://` page is cross-site vs `127.0.0.1`.
- Chrome applies **Lax by default** when no SameSite is set, so deleting the line changes nothing. Getting cross-site delivery needs `SameSite=None; Secure` (needs HTTPS).
- Same host, **different port** still counts as same-site.

## Tools
- `headcheck.py` now shows `X-Frame-Options: PRESENT: DENY` on the fixed site — found the gap and confirmed the fix with my own tool.
- Find click coordinates: `document.onmousemove = (e) => { document.title = e.clientX + ", " + e.clientY };`
- `python -m http.server` style mini server (`http.server`) to serve static attacker files.

## In my own words
-
-
-