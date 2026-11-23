import argparse
import re
import socket
import ssl
import sys
import time
from urllib.parse import urlparse

import requests
import certifi


# ---------- header grading (from headcheck2) ----------
# TODO: paste your grade_hsts, grade_csp, grade_xfo, grade_nosniff, and CHECKS here
def grade_hsts(value):
    if value is None:
        return "MISSING", "no HSTS header"
    match = re.search(r"max-age=(\d+)", value)
    age = int(match.group(1)) if match else 0
    if age < 15768000:        # ~6 months
        return "WEAK", f"max-age too low ({age})"
    return "STRONG", f"max-age={age}"


def grade_csp(value):
    if value is None:
        return "MISSING", "no CSP header"
    if "'unsafe-inline'" in value:
        return "WEAK", "allows 'unsafe-inline' (XSS protection weakened)"
    if "*" in value:
        return "WEAK", "uses wildcard source *"
    return "STRONG", "no unsafe-inline or wildcard"


def grade_xfo(value):
    if value is None:
        return "MISSING", "no X-Frame-Options"
    if value.upper() in ("DENY", "SAMEORIGIN"):
        return "STRONG", value
    return "WEAK", f"unusual value: {value}"


def grade_nosniff(value):
    if value is None:
        return "MISSING", "no X-Content-Type-Options"
    if value.lower() == "nosniff":
        return "STRONG", "nosniff"
    return "WEAK", f"unexpected value: {value}"

CHECKS = {
    "Strict-Transport-Security": grade_hsts,
    "Content-Security-Policy": grade_csp,
    "X-Frame-Options": grade_xfo,
    "X-Content-Type-Options": grade_nosniff,
}

def scan_headers(url):
    print("=== SECURITY HEADERS ===")
    try:
        r = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"  Could not fetch: {e}")
        return
    for header, grade_func in CHECKS.items():
        value = r.headers.get(header)
        status, reason = grade_func(value)
        print(f"  {status:8} {header}: {reason}")


# ---------- certificate (from certcheck / cert_fields) ----------
def get_issuer_org(cert):
    issuer = cert.get("issuer", ())
    for group in issuer:
        for key, value in group:    
            if key == "organizationName":
                return value

    return "Unknown"

def days_left(cert):
    expires = ssl.cert_time_to_seconds(cert["notAfter"])   # certificate date string → epoch seconds
    now = time.time()                                      # current time → epoch seconds

    seconds_left = expires - now
    return int(seconds_left // 86400)                 # 86400 = seconds in one day

def scan_certificate(hostname):
    print("\n=== TLS CERTIFICATE ===")
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
    except Exception as e:
        print(f"  Could not get certificate: {e}")
        return

    days = days_left(cert)
    issuer = get_issuer_org(cert)

    print(f"{days} days left")
    print(f"Issuer: {issuer}")

# ---------- cookies (from cookiecheck) ----------
def parse_cookie(line):
    parts = line.split(";")
    name = parts[0].split("=", 1)[0].strip()
    flags = []
    for part in parts[1:]:
        flags.append(part.strip().lower())
    return name, flags

def get_samesite(flags):
    for flag in flags:
        if flag.startswith("samesite="):
            return flag.split("=", 1)[1].strip()
    return "not set"

def scan_cookies(url):
    print("\n=== COOKIES ===")
    try:
        r = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"  Could not fetch: {e}")
        return
    lines = r.raw.headers.getlist("Set-Cookie")
    if not lines:
        print("  No cookies set")
        return

    for line in lines:
        name, flags = parse_cookie(line)
        secure = "secure" in flags
        httponly = "httponly" in flags
        samesite = get_samesite(flags)
        print(
            f"{name:<20} "
            f"Secure: {'yes' if secure else 'NO':<4} "
            f"HttpOnly: {'yes' if httponly else 'NO':<4} "
            f"SameSite: {samesite}"
        )
    return 

# ---------- DNS (from dnscheck) ----------
def scan_dns(hostname):
    print("\n=== DNS ===")
    try:
        results = socket.getaddrinfo(hostname, 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        print("  DNS lookup failed")
        return
    seen = []
    for family, _, _, _, sockaddr in results:
        version = "IPv4" if family == socket.AF_INET else "IPv6"
        entry = (version, sockaddr[0])
        if entry not in seen:
            seen.append(entry)
            print(f"  {version}: {sockaddr[0]}")


def main():
    parser = argparse.ArgumentParser(description="Security scanner — headers, TLS, cookies, DNS")
    parser.add_argument("url")
    args = parser.parse_args()

    # normalize: add https:// if missing, then get the hostname
    url = args.url
    if "://" not in url:
        url = "https://" + url
    hostname = urlparse(url).hostname

    print(f"\nScanning {url}  (host: {hostname})\n")
    scan_headers(url)
    scan_certificate(hostname)
    scan_cookies(url)
    scan_dns(hostname)
    print("\n=== SCAN COMPLETE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())