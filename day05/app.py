import secrets
from flask import Flask, request, make_response, redirect

app = Flask(__name__)

USERS = {"muhib": "pass123"}
SESSIONS = {}

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
    return "Hello from my own server"


@app.route("/whoami")
def whoami():
    print("--- a request arrived ---")
    print("Method:", request.method)
    print("Path:  ", request.path)
    print("Query: ", request.args)
    print("Agent: ", request.headers.get("User-Agent"))
    print("Cookie:", request.headers.get("Cookie"))
    return "Request received. Look at your terminal."


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return LOGIN_PAGE

    username = request.form.get("username")
    password = request.form.get("password")

    print("Form received:", request.form)

    if username in USERS and USERS[username] == password:
        session_id = secrets.token_hex(16)
        SESSIONS[session_id] = username
        print("Session table: ", SESSIONS)

        response = make_response(redirect("/dashboard"))
        response.set_cookie("session_id", session_id,
                            httponly=True, samesite="Lax")
        return response
    return "Wrong username or password", 401


@app.route("/dashboard")
def dashboard():
    session_id = request.cookies.get("session_id")
    username = SESSIONS.get(session_id)
    print("Cookie received:", session_id, "->", username)

    if not username:
        return "Please log in first", 401
    return f"""
    <p>Private dashboard of {username}</p>
    <form method="POST" action="/logout">
      <button>Log out</button>
    </form>
    """
@app.route("/logout", methods=["POST"])
def logout():
    session_id = request.cookies.get("session_id")
    SESSIONS.pop(session_id, None)

    response = make_response(redirect("/login"))
    response.delete_cookie("session_id")
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
