import sqlite3

db = sqlite3.connect("day11/users.db")
for row in db.execute("SELECT username, password_hash FROM users").fetchall():
    print(row)
db.close()