# Day 14 — Security Misconfiguration + Scanner

## Security misconfiguration
- Not one attack — a class of **setup/deployment mistakes** that hand attackers info or access for free. Common because invisible (nothing breaks).
- The main ones:
  1. **Debug mode in production** — error page leaks stack trace, source, file paths, and an interactive console that can run code. (Flask `debug=True`.)
  2. **Default credentials** (`admin/admin`) left unchanged.
  3. **Verbose errors** — a SQL error message reveals the injection point + schema.
  4. **Directory listing** enabled → browse backups, `.git`, configs.
  5. **Missing security headers** (HSTS/CSP/XFO).
  6. **Unnecessary features/ports/admin interfaces** exposed.
- Why attackers love it: pure **recon**, just look. Usually the **doorway** to the real attacks, not standalone.
- Debug leak seen: `?a=10&b=0` with `debug=True` → full traceback + debugger. `debug=False` → generic 500, no details.
- Lesson: **dev settings ≠ prod settings.** A deployment checklist (debug off, generic errors, no defaults, headers on) is itself a sellable audit deliverable.

## Upgraded headcheck — grade quality, not just presence
- "Present" ≠ "good": `HSTS max-age=0` disables it; CSP with `'unsafe-inline'` or `*` is weak.
- Three states now: **MISSING / WEAK / STRONG**, each with a reason.
```python
re.search(r"max-age=(\d+)", value)   # (\d+) = capture group; .group(1) = the number
```
- Pattern: one **grading function per header**, a `CHECKS` dict mapping header → grader → loop runs each. Add a header = write one function + one dict line.
- Real catch: flagged GitHub's CSP as WEAK (`'unsafe-inline'`). Honest framing: GitHub likely uses nonces/hashes to compensate → the finding is "review whether mitigated," not "vulnerable." **Tools surface for a human; they don't pronounce verdicts.**

## Scanner — one tool, one report
- Bundled headers + TLS cert (days-left, issuer) + cookies (Secure/HttpOnly/SameSite) + DNS (IPs) into `scanner.py`.
- Reused the clean single-purpose functions from Days 2 & 4 — the payoff of writing them separately.
- Deliberate duplication (self-contained deliverable) for now; Phase 4 = proper package.
- This combined output = a real "external security scan," and the seed of the audit product.

## In my own words
-
-
-