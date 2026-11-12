import argparse
import sys

import requests

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def fetch(url):
    r = requests.get(url, timeout=10)
    return r


def check_headers(headers):
    results = {}
    for name in SECURITY_HEADERS:
        value = headers.get(name)
        results[name] = value
    return results

def shorten(value, limit=80):
    if len(value) > limit:
        return value[:limit] + "..."
    return value


def main():
    parser = argparse.ArgumentParser(description="Check a site's security headers")
    parser.add_argument("url")
    args = parser.parse_args()

    try:
        response = fetch(args.url)
    except requests.exceptions.MissingSchema:
        print("Please include http:// or https://")
        return 1
    except requests.exceptions.InvalidURL:
        print("URL is invalid")
        return 1
    except requests.exceptions.Timeout:
        print("Site took too long to respond")
        return 1
    except requests.exceptions.SSLError:
        print("Site was reached, but its TLS certificate is invalid")
        return 1
    except requests.exceptions.ConnectionError:
        print("Site couldn't be reached")
        return 1
    except requests.exceptions.RequestException:
        print("request failed")
        return 1

    print("Final URL:", response.url)

    results = check_headers(response.headers)

    present = 0
    for name, value in results.items():
        if value is None:
            print(f"{name}: MISSING")
        else:
            print(f"{name}: PRESENT: {shorten(value)}")
            present += 1

    print(f"{present}/{len(SECURITY_HEADERS)} security headers present")

    return 0

if __name__ == "__main__":
    sys.exit(main())
