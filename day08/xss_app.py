import secrets
from flask import Flask, request, redirect
from markupsafe import escape
app = Flask(__name__)

SESSIONS = {}
comments = []

@app.after_request
def add_csp(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
    return response

@app.route("/")
def index():
    page = "<h2>Comment Board</h2>"
    page += """
    <form method="POST" action="/comment">
      <input name="text" placeholder="Your comment" style="width:300px">
      <button>Post</button>
    </form>
    <hr>
    """
    for c in comments:
        page += f"<div>{escape(c)}</div>"
    return page

@app.route("/comment", methods=["POST"])
def comment():
    text = request.form.get("text")
    comments.append(text)
    print("Comment posted:", text)
    return redirect("/")

@app.route("/login/<username>")
def login(username):
    session_id = secrets.token_hex(16)
    SESSIONS[session_id] = username
    from flask import make_response
    resp = make_response(redirect("/"))
    resp.set_cookie("session_id", session_id)      # note: NO httponly — that's the point
    return resp

@app.route("/whoami")
def whoami():
    username = SESSIONS.get(request.cookies.get("session_id"))
    return f"You are: {username}"

if __name__ == "__main__":
    app.run(port=5000, debug=True)