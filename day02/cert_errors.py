import ssl
from cert_fields import get_cert

hosts = [
    "example.com",
    "expired.badssl.com",
    "self-signed.badssl.com",
    "untrusted-root.badssl.com",
    "wrong.host.badssl.com",
]

for host in hosts:
    try:
        get_cert(host)
        print(f"{host}: OK")
    except ssl.SSLCertVerificationError as e:
        print(f"{host}: REJECTED - {e.verify_message}")
    except ssl.SSLError as e:
        print(f"{host}: TLS Error - {e}")
    except OSError as e:
        print(f"{host}: CONNECTION FAILED - {e}")

