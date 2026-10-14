import socket
import ipaddress

def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    try:
        ipaddress.ip_address(target)
    except ValueError:
        if target.replace(".", "").isdigit():
            return "Error: Invalid IP address"
        try:
            socket.gethostbyname(target)
        except socket.gaierror:
            return "Error: Invalid hostname"

    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((target, port)) == 0:
            open_ports.append(port)
        s.close()
    return open_ports