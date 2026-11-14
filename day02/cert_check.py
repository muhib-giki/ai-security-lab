import argparse
import ssl
import sys
from urllib.parse import urlparse

from cert_fields import get_cert, get_sans, get_issuer_org, days_left

OK = "OK"
WARNING = "WARNING"
INVALID = "INVALID"
ERROR = "ERROR"

def normalize_url(text):
    text = text.strip()
    if "://" not in text:
        text = "https://" + text
    return text

def get_hostname(text):
    parts = urlparse(normalize_url(text))
    if not parts.hostname:
        raise ValueError(f"Hostname not found in {text!r}")
    return parts.hostname

def check_host(host, warn_days):
    try:
        hostname = get_hostname(host)
    except ValueError as e:
        return ERROR, str(e)

    try: 
        cert = get_cert(hostname)
    except ssl.SSLCertVerificationError as e:
        return INVALID, e.verify_message
    except ssl.SSLError as e:
        return ERROR, f"TLS Error: {e}"
    except OSError as e:
        return ERROR, f"connection failed: {e}"

    days = days_left(cert)
    issuer = get_issuer_org(cert)
    names = ", ".join(get_sans(cert))
    details = f"{days} days left | {issuer} | {names}"

    if days < warn_days:
        return WARNING, details
    
    return OK, details

def main():
    parser = argparse.ArgumentParser(description="Check TLS certificate health")
    parser.add_argument("hosts", nargs="+")
    parser.add_argument("--warn-days", type=int, default=14)
    args = parser.parse_args()

    problems = 0
    for host in args.hosts:
        status, details = check_host(host, args.warn_days)
        print(f"{status:8} {host}: {details}")
        if status != OK:
            problems += 1

    if problems > 0:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())