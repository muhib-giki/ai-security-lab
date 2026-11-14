import argparse
import socket
import sys

from normalize import get_hostname

def resolve(hostname):
    results = socket.getaddrinfo(hostname, 443, proto=socket.IPPROTO_TCP)
    ips = []

    for family, _, _, _, sockaddr in results:
        version = "IPv4" if family == socket.AF_INET else "IPv6"
        entry = (version, sockaddr[0])
        if entry not in ips:
            ips.append(entry)
    return ips

def main():
    parser = argparse.ArgumentParser(description="Look up the IP addresses of hosts")
    parser.add_argument("hosts", nargs="+")
    args = parser.parse_args()

    failures = 0
    for host in args.hosts:  
        print(host)
        try:
            hostname = get_hostname(host)
            ips = resolve(hostname)
        except ValueError as e:
            print(f"ERROR: {e}")
            failures += 1
            continue
        except socket.gaierror as e:
            print("DNS lookup failed: name not found")
            failures += 1
            continue

        for version, ip in ips:
            print(f"{version}: {ip}")
        
        print()

    return 1 if failures > 0 else 0

if __name__ == "__main__":
    sys.exit(main())