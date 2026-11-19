# Day 9 — SQL Injection

## What it is
- User input glued into a SQL query string → input becomes **SQL code**, not data.
- Same root flaw as XSS, one layer deeper: **mixing untrusted data into code**. XSS = data into HTML; SQLi = data into a query.

## The vulnerable pattern
```python
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
```
- Input lands inside the quotes → an attacker can close the quote and rewrite the logic.

## Login bypass payloads (username box)
| Payload | Effect |
|---|---|
| `muhib' --` | `'` closes the string, `--` comments out the password check → logs in as muhib |
| `admin' --` | same, as admin — password never known |
| `' OR '1'='1' --` | makes the WHERE always true → logs in as first user |

- `--` starts a SQL comment: the rest of the line is ignored (SQLite needs a space after `--`).
- **Precedence:** `AND` binds tighter than `OR`. `' OR '1'='1` with a blank password can fail because it parses as `username='' OR ('1'='1' AND password='')`. The `--` version is reliable — it deletes the password half outright.

## UNION attack — steal the whole table
- `UNION` glues a second SELECT's results onto the first. Rule: **same number of columns**.
- Find column count by trial: `SELECT 1`, then `1,2`, ... until no error.
- `' UNION SELECT id, username, password, email FROM users --` → dumps every row.

## Discovering structure blind (real attacks don't know names)
- Databases describe themselves:
  - SQLite: `sqlite_master` (has table `name` and full `CREATE TABLE sql`).
  - MySQL/Postgres/MSSQL: `information_schema.tables` / `.columns`.
- `' UNION SELECT 1, name, sql, 4 FROM sqlite_master --` → reveals tables and columns.
- Real sequence: 1) find column count, 2) read structure, 3) read data.

## How attackers see results when the page shows nothing
- **In-band:** result appears in the page (the lab case). Easiest.
- **Blind — boolean:** inject a true/false condition, watch the page change; extract data one character at a time.
- **Blind — time-based:** make the DB `sleep(5)` when the answer is yes; read data by response timing.
- **Out-of-band:** force the DB to send data to attacker's server (DNS/HTTP).
- Key point: **the visible result is not required.** Any two distinguishable states (true/false, fast/slow) leak the whole DB. `sqlmap` automates all of this.

## The fix — parameterized queries
```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
rows = db.execute(query, (username, password)).fetchall()
```
- Query (with `?`) and values are passed **separately**. DB compiles the query structure first, then drops values in as **pure data**.
- Input can never become query structure → `' OR '1'='1' --` is searched as a literal username → no match.
- Same principle as Day 8 escaping: **keep data and code separate**, enforced by the DB.
- **Rule for life: never concatenate user input into SQL. Always use placeholders.** (`?`, `%s`, named params; ORMs do it automatically.)
- Audit habit: grep for user input concatenated into a query string.

## In a real system
- Passwords in the stolen table should be **hashed** (later day) — so a dumped table isn't instantly usable.
- ORMs (SQLAlchemy, Django, Prisma) parameterize by default; raw/`.raw()`/string-built queries are where SQLi still appears.

## In my own words
-
-
-