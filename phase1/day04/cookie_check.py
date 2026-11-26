import argparse
import sys

import requests


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


def main():
    parser = argparse.ArgumentParser(description="Check a site's cookie security settings")
    parser.add_argument("url")
    args = parser.parse_args()

    try:
        r = requests.get(args.url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return 1

    lines = r.raw.headers.getlist("Set-Cookie")
    if not lines:
        print("No cookies set")
        return 0

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
    return 0


if __name__ == "__main__":
    sys.exit(main())