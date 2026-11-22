# Day 13 — Command Injection

## What it is
- User input glued into an **OS command** string, run through the **shell** → input becomes OS commands.
- The ladder of injection (same root flaw, worse target each time):
  - XSS → code in the **browser**
  - SQLi → queries in the **database**
  - Command injection → commands on the **server's OS** → usually full server takeover (**RCE**).
- Most severe bug class. "Never let data become code," at the OS level.

## Why apps run commands
- ping/network tools, image conversion (ImageMagick), PDF generation, zip/tar, git. App builds a command string and runs it.

## The shell is the problem
- `shell=True` hands the whole string to the shell, which treats these as special:
  | char | meaning |
  |---|---|
  | `;` | run next command (Linux) |
  | `&` | run next command (Windows) |
  | `&&` | run next if first succeeded |
  | `\|` | pipe output into next |
  | `` ` `` / `$(...)` | run and substitute output |

## The attack (built)
- Feature: `ping -n 2 <host>` via `subprocess.run(cmd, shell=True)`.
- Payload in host box: `127.0.0.1 & whoami` → runs ping AND `whoami`.
- `whoami` = which user the server runs as (how much power you got; `system`/`root` = max).
- Also: `& dir`/`ls`, `& type file`/`cat`, `& ipconfig`, read files outside the app (`type C:\Windows\...\hosts`), write files (`echo ... > hacked.txt`).
- Writing files → plant a **web shell** = permanent backdoor that survives the patch.

## Blast radius (why it's #1 severity)
- Read any file the server user can (DB passwords, API keys, cloud creds, source).
- Write files (deface, backdoor). Run any program (malware, miners). Pivot to the internal network.

## The fix
**Layer 1 — no shell, arguments as a list:**
```python
subprocess.run(["ping", "-n", "2", host], shell=False, ...)
```
- `host` is passed to `ping` as **one literal argument**. No shell → `&` isn't special. `127.0.0.1 & whoami` becomes a bogus hostname, not two commands.
- **Same principle as SQL placeholders (Day 9):** keep data separate from code. Escaping (HTML) → placeholders (SQL) → argument lists (OS). One idea, three layers.

**Layer 2 — validate input to its expected shape:**
```python
if not re.match(r"^[a-zA-Z0-9.\-]+$", host):
    return "Invalid host.", 400   # rejects &, spaces, slashes
```

**Rules:**
- Never pass user input to a shell; avoid `shell=True` with user data.
- Better: don't shell out at all — use a library (image lib instead of calling ImageMagick). Most command injection exists because someone shelled out needlessly.
- Validate to the narrow allowed shape as a second layer.

## In my own words
-
-
-