from flask import Flask, request

app = Flask(__name__)


@app.route("/divide")
def divide():
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    return f"Result: {a / b}"


if __name__ == "__main__":
    app.run(port=5000, debug=False)      # debug ON — the misconfiguration