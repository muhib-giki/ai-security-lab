# Day 2 — HTTPS, TLS and certificates

## HTTPS = HTTP inside TLS
```
HTTP  (same text as Day 1)
TLS   (encryption + identity)
TCP   (the connection)
```

## TLS: three guarantees
1. **Confidentiality** — nobody can read it.
2. **Integrity** — nobody can change it unnoticed.
3. **Authentication** — you're talking to the real server (via certificates).
- Encryption without authentication is worthless: you'd have a secure tunnel **to the attacker**.

## Handshake (simplified)
1. ClientHello — versions, ciphers, and **SNI** (the site name, sent in **plain text**).
2. Server picks settings, sends its certificate (chosen by SNI).
3. Client verifies the certificate.
4. Key exchange (Diffie-Hellman) — shared secret without sending it.
5. Encrypted HTTP.

**HTTPS hides:** path, headers, cookies, body.
**Still visible:** server IP, **domain name** (SNI + DNS), timing, data size.

## Certificates
| Field | Meaning |
|---|---|
| SANs | Names the cert is valid for — **browsers check SANs, not Common Name** |
| Issuer | The CA that signed it |
| notBefore / notAfter | Validity window |
| Public key + signature | Proof it's genuine |

- **Wildcard `*.x.com`** matches exactly **one** level (`a.x.com` yes, `a.b.x.com` no, `x.com` no).
- ~90-day lifetimes now normal and shrinking → renewal must be automated → expiry monitoring has real value.

## Chain of trust
`Root CA → Intermediate CA → Leaf (site)`
- Server sends leaf + intermediate; client must already have the root.
- **Every root is self-signed.** It's trusted only because it's **preinstalled** in the trust store.
- Whoever can add a root to your machine (employer, antivirus, malware) can intercept HTTPS.
- Trust stores differ: `requests` uses **certifi**; Python `ssl` on Windows uses the **Windows store** (missing roots → "unable to get local issuer certificate").

## DV / OV / EV
- **DV** = CA only checked domain control. Phishing sites get free DV certs.
- **Padlock = encrypted + authenticated to this domain. Not "this site is trustworthy".**

## Certificate failures (reject all of them)
| Failure | Python message |
|---|---|
| Expired | `certificate has expired` |
| Self-signed | `self-signed certificate` |
| Untrusted root | `self-signed certificate in certificate chain` |
| Wrong host | `Hostname mismatch` |
| Revoked | Not checked by Python by default — revocation is messy industry-wide |

- **Never** use `verify_mode = CERT_NONE` / `check_hostname = False` / `verify=False`. That's a vulnerability.
- HSTS sites remove the browser's "proceed anyway" button.
- Wrong system clock → all certs look invalid.

## Debug by layer
| Layer | Error |
|---|---|
| DNS | `socket.gaierror` (name not found) |
| TCP | `TimeoutError`, `ConnectionRefusedError` |
| TLS | `ssl.SSLError`, `ssl.SSLCertVerificationError` |
| HTTP | Status codes |
- A single timeout → retry before concluding anything.
- In `requests`, `SSLError` is a kind of `ConnectionError` — catch it **first**.

## Python
```python
context = ssl.create_default_context(cafile=certifi.where())
ssock = context.wrap_socket(sock, server_hostname=host)   # SNI + name check
cert = ssock.getpeercert()                                 # verified cert as dict
ssl.cert_time_to_seconds(cert["notAfter"]) - time.time()   # seconds left
```
- `except X as e:` gives the exception object (`e.verify_message`).
- Exception families: `OSError` > `ssl.SSLError` > `SSLCertVerificationError`. Specific first.
- One-item tuple needs a trailing comma: `(5,)`.
- Status values as **constants** (`WARNING = "WARNING"`) — typos become loud errors, not silent bugs.
- argparse: `nargs="+"` for a list, `--flag` with `type=int, default=...`.

## In my own words
-
-
-