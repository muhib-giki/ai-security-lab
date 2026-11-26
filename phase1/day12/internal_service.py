from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Internal service. If you can read this, you're inside the network."

@app.route("/admin/secret-keys")
def secret_keys():
    # no auth — the developers assumed only internal services could ever reach this
    return "TOP SECRET: database_password=prod_db_7f3a, api_key=sk_live_9981"


if __name__ == "__main__":
    app.run(port=8080, debug=True)