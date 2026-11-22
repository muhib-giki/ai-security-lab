# Day 12 — SSRF (Server-Side Request Forgery)

## The idea
- Trick the **server** into fetching a URL **you** choose.
- Key insight: when you fetch a URL, the request comes from the internet. When the **server** fetches it, the request comes from **inside the server's network** — past the firewall.
- So SSRF reaches things you can't: `127.0.0.1` services on the server, internal IPs (`10.x`, `192.168.x`), internal hostnames, and cloud metadata.
- Internal services often have **weak/no auth** ("only internal systems can reach us") → SSRF turns the vulnerable app into a **proxy** aimed inside.

## Where it hides in real apps (the real skill)
- There is NO "paste internal URL" box in the wild. The server-side fetch is **disguised** inside normal features:
  - image/avatar "from URL", import-from-URL, **webhooks**, link previews, PDF/invoice generators, "test this integration/callback URL".
- Attacker workflow: map the app (Burp) → find any param holding a URL/host (`url`, `image_url`, `callback`, `webhook`, `src`, `endpoint`) → point it inward or at a server you control → watch for a hit (**blind SSRF** = detect via callback, not response) → escalate.
- Example: change `"image_url": "https://shop.com/x.jpg"` → `"http://127.0.0.1:8080/admin"`. Looks innocent; it's SSRF.

## Cloud metadata — the dangerous version
- Cloud servers query a magic internal address for info about themselves: `http://169.254.169.254/`.
- It hands out the server's **temporary cloud credentials** (so keys aren't hardcoded). Reachable only from inside the instance.
- SSRF → make the server fetch metadata → **steal the cloud identity** → access the account's storage/DBs.
- AWS creds path: `/latest/meta-data/iam/security-credentials/<role>`.
- **Capital One 2019:** SSRF → metadata → 100M+ records. (AWS IMDSv2 mitigates, but old setups remain.)

## The fix
**Wrong: blocklist bad addresses.** Endless bypasses:
- `localhost`, `0.0.0.0`, `127.1`, `[::1]`, decimal `2130706433`, and a **public domain whose DNS resolves to an internal IP** (`127.0.0.1.nip.io`). Can't enumerate all bad values (same lesson as open redirect).

**Right:**
1. **Allowlist** known-good destinations when possible (deny by default).
2. When arbitrary external URLs are needed: **resolve the hostname to its IP, then block if the IP is internal** — defeats the DNS trick by checking where the name actually points.
```python
hostname = urlparse(url).hostname
ip = socket.gethostbyname(hostname)
ip_obj = ipaddress.ip_address(ip)
if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
    return False   # blocked
```
- Internal ranges: `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16` (metadata).

## Expert caveat — DNS rebinding (TOCTOU)
- Code resolves once to check, `requests` resolves again to connect. Attacker makes DNS return a safe IP first, dangerous IP second.
- Full fix: resolve once, force the connection to that exact IP. (Naming it = depth.)

## Bridge to networking
- SSRF is an **app** flaw (unvalidated URL input) whose **impact is all about the network** the server sits in. Ties directly to Day 3 (URLs, DNS, 127.0.0.1 vs localhost).

## In my own words
-
-
-