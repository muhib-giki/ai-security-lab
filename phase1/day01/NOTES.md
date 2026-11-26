# Day 1 — HTTP

## HTTP is just text
```
GET /path HTTP/1.1        ← request line: method, path, version
Host: example.com         ← headers: Name: value
Connection: close
                          ← blank line = end of headers (body comes after)
```
- Every line ends with `\r\n`.
- The server only knows what you send. Everything in a request is attacker-controllable.

## Status code families
| | Meaning |
|---|---|
| 2xx | Success (200) |
| 3xx | Go elsewhere (301, 302) |
| 4xx | Client's fault (400, 404, 405) |
| 5xx | Server broke (500, 502, 503) |

## Key ideas
- **Host header** — one IP hosts many sites (virtual hosting); the name isn't sent by TCP, so Host tells the server which site. Attack: **Host header injection** (poisoned password-reset links).
- **Methods are just words.** Server decides what it accepts; 405 + `Allow:` header. Testers try other methods to bypass access control.
- **Redirects** — server sends 3xx + `Location`; the **client** chooses to follow.
  - **Open redirect:** server copies user input into `Location` → phishing via a trusted domain.
  - Naive checks fail: "contains mybank.com" → `mybank.com.evil.com`; "starts with /" → `//evil.com`.
  - Fix: **allowlist** of destinations, or parse the URL and compare the real domain exactly.
- **Keep-alive vs close** — keep-alive reuses the connection. Clients know the body ended via `Content-Length`, not by waiting for a hang-up.
- **`recv()`** returns data, **blocks** if nothing yet, returns `b""` only when the server closes.

## Plain HTTP on a network = readable + changeable
- **MITM:** attacker on Wi-Fi can read and alter traffic.
- **SSL stripping:** attacker keeps you on HTTP while talking HTTPS to the real site.
- The HTTP→HTTPS redirect itself travels unprotected. Real fix is **HSTS**.

## Security headers
| Header | Protects against |
|---|---|
| `Strict-Transport-Security` | SSL stripping / MITM. `max-age`, `includeSubDomains`, `preload` (built-in browser list) |
| `Content-Security-Policy` | XSS (allowlist of script sources) |
| `X-Frame-Options` | Clickjacking |
| `X-Content-Type-Options: nosniff` | Files run as the wrong type |
| `Referrer-Policy` | Leaking private URLs |

- Missing header = missing **layer**, not automatically a vulnerability.
- **Severity = missing control × what's at stake on that page.** Never oversell findings.
- **Present ≠ good:** `max-age=0` turns HSTS off; `default-src *` is a near-useless CSP.

## Python
- `str` is for humans, `bytes` for networks: `.encode()` → bytes, `.decode()` → str.
- `with ... as x:` auto-closes resources.
- `d.get(key)` returns `None` if missing; `d[key]` crashes (`KeyError`). Test the unhappy path.
- Always set `timeout=` on network calls.
- `try/except`: specific exceptions first, broad last. Never bare `except:`.
- Exit codes: `0` = success, non-zero = failure (CI reads these). `sys.exit(main())`.
- `if __name__ == "__main__":` → code runs only when the file is run directly, not when imported.
- Output must never mislead the reader (e.g. show `...` when truncating).

## Commands
- Exit code — PowerShell: `echo $LASTEXITCODE` · Bash: `echo $?` (check immediately after).

## In my own words
-
-
-