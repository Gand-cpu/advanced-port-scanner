# advanced_port_scanner.py

import socket
import threading
import argparse

print_lock = threading.Lock()

def scan_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip, port))
        try:
            banner = s.recv(1024).decode().strip()
        except:
            banner = "No banner"
        with print_lock:
            print(f"[+] Port {port} is OPEN  |  Banner: {banner}")
        s.close()
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description="Multithreaded Port Scanner with Banner Grabbing")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1000)", default="1-1024")
    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("[-] Invalid hostname")
        return

    start_port, end_port = map(int, args.ports.split("-"))

    print(f"\n[~] Scanning {ip} from port {start_port} to {end_port}...\n")

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n[+] Scan complete.")

if __name__ == "__main__":
    main()
