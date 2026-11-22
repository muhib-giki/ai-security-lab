import re
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>Network Tools — Ping a host</h2>
    <form method="POST" action="/ping">
      <input name="host" placeholder="e.g. google.com" style="width:300px">
      <button>Ping</button>
    </form>
    """

@app.route("/ping", methods=["POST"])
def ping():
    host = request.form.get("host")

    # Layer 2: validate — only allow hostname/IP characters
    if not re.match(r"^[a-zA-Z0-9.\-]+$", host):
        return "Invalid host.", 400

    # Layer 1: no shell, arguments passed as a list
    command = ["ping", "-n", "2", host]
    print("Running command:", command)

    result = subprocess.run(command, shell=False, capture_output=True, text=True)
    return f"<pre>{result.stdout}\n{result.stderr}</pre>"


if __name__ == "__main__":
    app.run(port=5000, debug=True)