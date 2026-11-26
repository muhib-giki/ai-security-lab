import sys
from urllib.parse import urlparse

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

def main():
    tests = [
        "example.com",
        "  https://github.com/login  ",
        "EXAMPLE.com/path?x=1",
        "http://example.com",
        "github.com:8443",
        "https://",
    ]

    for test in tests:
        try:
            print(f"{test!r} -> {normalize_url(test)} -> {get_hostname(test)}")
        except ValueError as e:
            print(f"{test!r} -> ERROR: {e}") 


if __name__ == "__main__":
    main()