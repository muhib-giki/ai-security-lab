import secrets

from flask import Flask, request, make_response, redirect

app = Flask(__name__)

USERS = {"muhib": "pass123"}
EMAILS = {"muhib": "muhib@real.com"}      # username -> current email
SESSIONS = {}                              # session id -> username
CSRF_TOKENS = {}      # session_id -> csrf token

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
    if username in USERS and USERS[username] == password:
        session_id = secrets.token_hex(16)
        SESSIONS[session_id] = username
        response = make_response(redirect("/settings"))
        response.set_cookie("session_id", session_id, httponly=True, samesite="Lax")
        return response
    return "Wrong username or password", 401


@app.route("/settings")
def settings():
    session_id = request.cookies.get("session_id")
    username = SESSIONS.get(session_id)
    if not username:
        return "Please log in first", 401

    token = secrets.token_hex(16)
    CSRF_TOKENS[session_id] = token

    current = EMAILS.get(username)
    return f"""
    <h2>Settings for {username}</h2>
    <p>Current email: <b>{current}</b></p>
    <form method="POST" action="/change-email">
      <input type="hidden" name="csrf_token" value="{token}">
      <input name="email" placeholder="New email">
      <button>Change email</button>
    </form>
    """

@app.route("/change-email", methods=["POST"])
def change_email():
    session_id = request.cookies.get("session_id")
    username = SESSIONS.get(session_id)
    if not username:
        return "Please log in first", 401

    sent_token = request.form.get("csrf_token")
    real_token = CSRF_TOKENS.get(session_id)
    if not sent_token or sent_token != real_token:
        print(f"!!! CSRF BLOCKED for {username} !!!")
        return "CSRF check failed", 403

    new_email = request.form.get("email")
    EMAILS[username] = new_email
    print(f"!!! EMAIL CHANGED for {username}: now {new_email} !!!")
    return f"Email updated to {new_email}"

if __name__ == "__main__":
    app.run(port=5000, debug=True)