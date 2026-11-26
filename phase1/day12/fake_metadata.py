from flask import Flask

app = Flask(__name__)


@app.route("/latest/meta-data/iam/security-credentials/web-server-role")
def credentials():
    return """{
  "AccessKeyId": "ASIA_FAKE_STOLEN_KEY",
  "SecretAccessKey": "fakeSecret_ThisWouldUnlockTheCloudAccount",
  "Token": "FAKE_SESSION_TOKEN_abc123"
}"""


if __name__ == "__main__":
    app.run(port=169, debug=True)