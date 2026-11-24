import sqlite3
import secrets
import subprocess

import bcrypt
from flask import Flask, request, make_response, redirect

app = Flask(__name__)
SESSIONS = {}


def setup():
    db = sqlite3.connect("day15/app.db")
    db.execute("DROP TABLE IF EXISTS users")
    db.execute("CREATE TABLE users (id INTEGER, username TEXT, password_hash TEXT, role TEXT, api_token TEXT)")
    for uid, user, pw, role in [
        (1, "muhib", "pass123", "user"),
        (2, "alice", "alicepw", "user"),
        (3, "admin", secrets.token_hex(8), "admin"),
    ]:
        h = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        token = secrets.token_hex(16)
        db.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (uid, user, h, role, token))
    db.commit()
    db.close()


def current_user(req):
    return SESSIONS.get(req.cookies.get("session_id"))


@app.route("/")
def home():
    return '<h2>SecureNotes</h2><a href="/login">Login</a>'


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
        <form method="POST">
          <input name="username" placeholder="user">
          <input name="password" type="password">
          <button>Login</button>
        </form>"""
    username = request.form.get("username")
    password = request.form.get("password")
    db = sqlite3.connect("day15/app.db")
    row = db.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,)).fetchone()
    db.close()
    if row and bcrypt.checkpw(password.encode(), row[0]):
        sid = secrets.token_hex(16)
        SESSIONS[sid] = username
        resp = make_response(redirect("/dashboard"))
        resp.set_cookie("session_id", sid, httponly=True)
        return resp
    return "Login failed", 401


@app.route("/dashboard")
def dashboard():
    user = current_user(request)
    if not user:
        return "Please log in", 401
    return f'<h3>Welcome {user}</h3><a href="/profile/1">My profile</a> | <a href="/admin/tools">Admin tools</a>'


@app.route("/profile/<int:user_id>")
def profile(user_id):
    user = current_user(request)
    if not user:
        return "Please log in", 401
    db = sqlite3.connect("day15/app.db")
    row = db.execute("SELECT username, role, api_token FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    if not row:
        return "Not found", 404
    return f"<h3>Profile</h3>Username: {row[0]}<br>Role: {row[1]}<br>API token: {row[2]}"


@app.route("/admin/tools")
def admin_tools():
    user = current_user(request)
    if not user:
        return "Please log in", 401
    return """
    <h3>Admin Tools</h3>
    <form method="POST" action="/admin/backup">
      <input name="filename" placeholder="backup name">
      <button>Create backup</button>
    </form>"""


@app.route("/admin/backup", methods=["POST"])
def admin_backup():
    user = current_user(request)
    if not user:
        return "Please log in", 401
    filename = request.form.get("filename")
    command = "echo backup created > " + filename
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return f"<pre>Backup done: {filename}\n{result.stdout}{result.stderr}</pre>"


if __name__ == "__main__":
    setup()
    # create the target secret file
    with open("day15/flag.txt", "w") as f:
        f.write("FLAG{you_chained_the_vulnerabilities}")
    app.run(port=5000, debug=True)