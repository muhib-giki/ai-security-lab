import sqlite3
import secrets

import bcrypt
from flask import Flask, request, make_response, redirect

app = Flask(__name__)

SESSIONS = {}
FAILED_ATTEMPTS = {}      # username -> number of recent failures
MAX_ATTEMPTS = 5

users = [
    ("muhib", "pass123"),
    ("huda", "pass124"),
    ("emad", "pass123"),
    ("humza", "pass125"),
]

def setup_database():
    db = sqlite3.connect("day11/users.db")
    db.execute("DROP TABLE IF EXISTS users")
    db.execute("CREATE TABLE users (username TEXT, password_hash TEXT)")

    for username, password in users:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        db.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))

    db.commit()
    db.close()

LOGIN_PAGE = """
<h2>Login</h2>
<form method="POST" action="/login">
  <input name="username" placeholder="Username">
  <input name="password" type="password" placeholder="Password">
  <button>Log in</button>
</form>
"""
@app.route("/")
def home():
    return '<h2>Home</h2><p><a href="/login">Go to login</a></p>'

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return LOGIN_PAGE

    username = request.form.get("username")
    password = request.form.get("password")

    if FAILED_ATTEMPTS.get(username, 0) >= MAX_ATTEMPTS:
        print(f"LOCKED OUT: {username}")
        return "Too many failed attempts. Account locked.", 429
    
    db = sqlite3.connect("day11/users.db")
    row = db.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    db.close()

    if row and bcrypt.checkpw(password.encode(), row[0]):
        FAILED_ATTEMPTS[username] = 0          # reset on success
        session_id = secrets.token_hex(16)
        SESSIONS[session_id] = username
        resp = make_response(f"Welcome, {username}")
        resp.set_cookie("session_id", session_id, httponly=True, samesite="Lax")
        return resp

    # count the failure
    FAILED_ATTEMPTS[username] = FAILED_ATTEMPTS.get(username, 0) + 1
    return "Wrong username or password", 401

if __name__ == "__main__":
    setup_database()
    app.run(port=5000, debug=True)