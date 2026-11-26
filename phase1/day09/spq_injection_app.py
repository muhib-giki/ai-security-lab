import sqlite3
from flask import Flask, request

app = Flask(__name__)

def setup_database():
    db = sqlite3.connect("day09/users.db")
    db.execute("DROP TABLE IF EXISTS users")
    db.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT, email TEXT)")
    db.execute("INSERT INTO users VALUES (1, 'muhib', 'pass123', 'muhib@real.com')")
    db.execute("INSERT INTO users VALUES (2, 'alice', 'alicepw', 'alice@real.com')")
    db.execute("INSERT INTO users VALUES (3, 'admin', 'supersecret', 'admin@real.com')")
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return LOGIN_PAGE

    username = request.form.get("username")
    password = request.form.get("password")

    query = "SELECT * from users where username = ? AND password = ?"
    print("Running query:", query)

    db = sqlite3.connect("day09/users.db")
    rows = db.execute(query, (username, password)).fetchall()

    db.close()

    if rows:
        return f"Logged in! Rows returned: {rows}"
    return "Wrong username or password", 401

if __name__ == "__main__":
    setup_database()
    app.run(port=5000, debug=True)
