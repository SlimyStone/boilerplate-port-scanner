import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from common_ports import ports_and_services


def _port_offen(ip, port):
    s = socket.socket()
    s.settimeout(1)
    try:
        return s.connect_ex((ip, port)) == 0
    finally:
        s.close()


def get_open_ports(target, port_range, verbose=False):
    ip = target
    hostname = None

    try:
        ipaddress.ip_address(target)
        try:
            hostname = socket.gethostbyaddr(target)[0]
        except (socket.herror, socket.gaierror):
            hostname = None
    except ValueError:
        if target.replace(".", "").isdigit():
            return "Error: Invalid IP address"
        try:
            ip = socket.gethostbyname(target)
            hostname = target
        except socket.gaierror:
            return "Error: Invalid hostname"

    ports = list(range(port_range[0], port_range[1] + 1))
    with ThreadPoolExecutor(max_workers=100) as pool:
        ergebnisse = list(pool.map(lambda p: _port_offen(ip, p), ports))
    open_ports = [p for p, offen in zip(ports, ergebnisse) if offen]

    if not verbose:
        return open_ports

    if hostname:
        header = f"Open ports for {hostname} ({ip})"
    else:
        header = f"Open ports for {ip}"
    lines = [header, "PORT     SERVICE"]
    for port in open_ports:
        lines.append(f"{port:<9}{ports_and_services.get(port)}")
    return "\n".join(lines)