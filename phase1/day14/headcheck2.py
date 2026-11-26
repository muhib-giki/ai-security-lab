import argparse
import sys
import re

import requests


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


def main():
    parser = argparse.ArgumentParser(description="Grade a site's security headers")
    parser.add_argument("url")
    args = parser.parse_args()

    try:
        r = requests.get(args.url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return 1

    print(f"Final URL: {r.url}\n")
    for header, grade_func in CHECKS.items():
        value = r.headers.get(header)
        status, reason = grade_func(value)
        print(f"{status:8} {header}: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())