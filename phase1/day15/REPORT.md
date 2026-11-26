# Security Assessment Report — SecureNotes

**Target:** SecureNotes web application
**Assessment type:** Grey-box web application penetration test
**Tester:** Muhibullah
**Date:** 2026-11-24

---

## Executive Summary

A standard, low-privileged user account can fully compromise the SecureNotes server by chaining three vulnerabilities. Starting from an ordinary login, an attacker can reach an administrative function they are not authorized to use, execute arbitrary operating-system commands through it, and read any file on the server — demonstrated by retrieving a protected file (`flag.txt`). A separate flaw leaks other users' API tokens, including the administrator's.

Two findings are rated **Critical/High** and require immediate remediation. The combination represents a full server compromise reachable by anyone who can create an account.

| # | Finding | Severity |
|---|---------|----------|
| 1 | Broken Access Control on Admin Functions | High |
| 2 | OS Command Injection in Backup Feature | Critical |
| 3 | Insecure Direct Object Reference (IDOR) on Profiles | High |

---

## Finding 1 — Broken Access Control on Admin Functions

- **Severity:** High
- **Location:** `GET /admin/tools`, `POST /admin/backup`
- **Description:** These endpoints verify that a user is authenticated (logged in) but do not verify that the user holds the `admin` role. The authorization check is missing entirely.
- **Impact:** Any standard user can perform administrative actions they are not authorized for, including the server backup function. Via Finding 2, this directly leads to full server compromise.
- **Reproduction:**
  1. Log in as a standard user (`muhib` / `pass123`).
  2. Navigate directly to `/admin/tools`.
  3. The admin-only page loads and is fully usable, despite the account not being an admin.
- **Remediation:** Enforce a role check on every administrative endpoint, not just authentication. After confirming the user is logged in, reject the request unless the user's role is `admin` (HTTP 403). Apply this to both `/admin/tools` and `/admin/backup`.

---

## Finding 2 — OS Command Injection in Backup Feature

- **Severity:** Critical
- **Location:** `POST /admin/backup`, `filename` parameter
- **Description:** The `filename` value supplied by the user is concatenated directly into a shell command string, which is then executed with `shell=True`. Shell metacharacters (`&`, `;`, `|`) in the input are interpreted by the shell, allowing the attacker to run arbitrary commands alongside the intended one.
- **Impact:** This is Remote Code Execution (RCE) — the most severe outcome in web security. An attacker can read any file the server process can access (database, configuration, credentials, source code), write files (including planting a persistent backdoor), run any program, and pivot to other machines on the internal network. Combined with Finding 1, this is reachable by any standard user.
- **Reproduction:**
  1. Log in as a standard user (`muhib` / `pass123`).
  2. Open `/admin/tools` (reachable due to Finding 1).
  3. In the `filename` field (which submits to `/admin/backup`), enter: `x & type day15\flag.txt`
  4. The response returns the contents of the protected file: `FLAG{you_chained_the_vulnerabilities}`.
  - **Operational note:** the underlying command uses `>` (output redirect), which overwrites the target filename. A payload that reuses the target file as the dummy write-target will destroy the file before it can be read. Always use a throwaway dummy name (e.g. `x`) for the echo target.
- **Remediation:** Never build shell commands by concatenating user input. Pass the command and its arguments as a list with `shell=False`, so user input is treated as literal data, never as shell syntax. Better still, avoid invoking a shell at all — perform the backup using native file APIs rather than an OS command. As a secondary layer, validate `filename` against a strict allowlist of permitted characters.

---

## Finding 3 — Insecure Direct Object Reference (IDOR) on Profiles

- **Severity:** High
- **Location:** `GET /profile/<id>`
- **Description:** The profile endpoint returns the record matching the `<id>` in the URL after checking only that the requester is logged in. It does not verify that the requested profile belongs to the requesting user. Changing the ID returns other users' records.
- **Impact:** An authenticated attacker can read any user's profile by incrementing the ID. The profile exposes each user's API token, so the attacker can harvest other users' tokens — including the administrator's — enabling further account takeover and providing an alternate escalation path.
- **Reproduction:**
  1. Log in as a standard user (`muhib`, id 1).
  2. Request `/profile/2`, `/profile/3`, etc.
  3. Each returns another user's username, role, and API token.
- **Remediation:** Enforce an ownership check: confirm the requested profile ID belongs to the logged-in user before returning it (otherwise 403/404). If administrators are intended to view all profiles, gate that access behind an explicit role check. Additionally, avoid returning secrets such as API tokens in profile responses at all.

---

## Attack Chain

The findings are far more severe in combination than in isolation. Starting from a standard user account:

1. **Finding 1** (broken access control) grants access to the admin backup tool, which the account should not be able to reach.
2. **Finding 2** (command injection) in that tool allows execution of arbitrary OS commands.
3. Chained, a low-privileged user achieves **full server compromise** and can read arbitrary files — demonstrated by retrieving `flag.txt`.

Separately, **Finding 3** leaks the administrator's API token, providing an independent path to privilege escalation. Neither the access-control flaw nor the command injection is exploitable to this extent alone; it is their combination that turns three medium-looking issues into a complete takeover.

---

## Remediation Priority

1. **Immediate:** Fix Finding 2 (command injection) — it is the mechanism of full compromise.
2. **Immediate:** Fix Finding 1 (access control) — it is the entry point to Finding 2.
3. **High:** Fix Finding 3 (IDOR) and stop returning API tokens in responses.