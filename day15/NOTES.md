# Day 15 — Capstone: Chaining Vulnerabilities

## What this was
- A realistic multi-feature app. Goal: start as a normal user, read a protected file (`flag.txt`) on the server.
- No single bug does it — the **chain** does. This is how real breaches work: several medium bugs, devastating together.

## The workflow (a real engagement in miniature)
1. **Recon** — map pages/URLs/inputs before attacking. Ask of each: does it trust me more than it should?
2. Find the weaknesses.
3. **Chain** them to the goal.
4. Write the **findings report** (the real deliverable).

## The chain I used
1. **Broken access control** — `/admin/tools` + `/admin/backup` checked only "logged in?", not role → a normal user reaches the admin backup tool.
2. **Command injection** — that tool glued `filename` into a shell command (`shell=True`) → inject `x & type day15\flag.txt`.
3. **Read the flag** → full server compromise from a standard account.
- Separate path: **IDOR** on `/profile/<id>` leaked every user's API token (incl. admin).

## Lessons earned the hard way
- **`>` overwrites files.** Payload `flag & type flag` ran `echo backup created > flag` first → **destroyed** the target, then read back my own echo ("backup created", not the flag). In a real test this could delete evidence or corrupt production. → Always use a throwaway dummy write-target (`x`), never the file you want to read.
- **Getting the flag isn't the point — knowing exactly why the payload worked is.** "It worked but I don't know why" is worthless in a report.
- Wrong filename (`flag.txt` vs `flag`) caused "cannot find the file specified" — the injection was fine; the path/name was wrong.

## Findings-report structure (what clients pay for)
- **Executive summary** (non-technical, read first) + severity table.
- Per finding: **Severity, Location, Description, Impact, Reproduction, Remediation.**
- **Attack Chain** paragraph — how findings combine.
- **Remediation priority** — what to fix first.
- Rules: state worst-case impact plainly (say "RCE"); reproduction must work verbatim; findings reference each other; be specific not generic.

## Portfolio artifacts from Phase 1
- The vulnerable apps + attack scripts + fixes (days 1–15).
- `scanner.py` — working external security scanner.
- `REPORT.md` — a real pentest findings report.

## In my own words
-
-
-