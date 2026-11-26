# Day 3 — URLs and DNS

## Parts of a URL
```
https://alice:secret@shop.example.com:8443/products/view?id=42&sort=asc#reviews
scheme   userinfo         host        port     path          query     fragment
```
- **Host** decides where you actually go.
- **Port** missing → 80 for http, 443 for https.
- **Fragment** (`#...`) is never sent to the server.
- **Query** is sent, and leaks into logs, history and the `Referer` header. **Never put secrets in URLs.**
- Host is case-insensitive; path usually is case-sensitive (`/admin` vs `/ADMIN` filter bypasses).

## URL tricks
| URL | Real host |
|---|---|
| `https://mybank.com@evil.com/login` | `evil.com` (text before `@` is just a username) |
| `//evil.com/path` | `evil.com` (scheme-relative) |
| `example.com/login` | none — parser reads it all as a path |

- `?q=a&q=b` → both values kept. Filter reads one, app reads the other = **parameter pollution**.

## The rule
- **Never make security decisions with string checks** (`in`, `startswith`). Parse the URL, then compare the **hostname** exactly.
- Use `hostname`, never `netloc` (netloc still contains the `user@` part).
- Parsers can disagree with browsers (e.g. `/\evil.com`), so for redirects the strongest fix is an **allowlist of fixed destinations**.

## Input normalization
- Users paste anything: bare names, full URLs, capitals, stray spaces.
- Strip → add `https://` if no scheme → parse → take hostname.
- If input can't be handled, **raise a clear error**. Never silently ignore part of the input (e.g. a port).

## DNS in five ideas
1. A **server** is just a computer that's always on.
2. An **IP address** is its number (IPv4 short, IPv6 long).
3. A **port** is which program on it (80, 443).
4. A **domain name** is a label for humans; **DNS** turns it into the IP.
5. The domain owner writes the record (**A record** = name → IP); a **resolver** looks it up and remembers the answer for a while (why DNS changes take time).

- A site can have several IPs, and different people can get different IPs for the same name.
- **Security:** a faked DNS answer sends you to the attacker's computer. The certificate check (Day 2) catches it. Two layers = **defense in depth**.

## The full journey of `https://github.com/login`
1. Parse the URL
2. DNS: name → IP
3. TCP: connect to IP on port 443
4. TLS: handshake + certificate check
5. HTTP: request and response

## Python
```python
from urllib.parse import urlparse, parse_qs
parts = urlparse(url)          # .scheme .hostname .port .path .query .fragment .username
parse_qs(parts.query)          # {'id': ['42']}  values are lists

socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)   # DNS lookup; fails with socket.gaierror
```
- `.strip()` removes whitespace from both ends.
- **Truthiness:** `None`, `''`, `0`, `[]`, `{}` count as false → `if not parts.hostname:`
- `raise ValueError("...")` when a function can't do its job; better than returning `None`.
- `{text!r}` shows quotes and hidden spaces.
- `_` for values you don't need when unpacking.
- `a if condition else b` picks one of two values.
- `continue` skips to the next loop item.
- A function with no `return` gives back `None`.
- Two tracebacks joined by "During handling of the above exception" → fix the **last** one.

## Commands
- `nslookup github.com` — DNS lookup from the terminal.

## In my own words
-
-
-