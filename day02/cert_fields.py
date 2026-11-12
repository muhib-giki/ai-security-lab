import socket
import ssl
import time

import certifi

def get_cert(host):
    context = ssl.create_default_context(cafile=certifi.where())
    with socket.create_connection((host, 443), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            return ssock.getpeercert()

def get_sans(cert):
    names = []
    sans = cert.get("subjectAltName", ())

    for kind, name in sans:
        if kind == "DNS":
            names.append(name)

    return names

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

if __name__ == "__main__":
    for host in ["example.com", "github.com"]:
        cert = get_cert(host)
        print(host)
        print("  SANs:     ", get_sans(cert))
        print("  Issuer:   ", get_issuer_org(cert))
        print("  Days left:", days_left(cert))