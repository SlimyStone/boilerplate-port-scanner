import socket

def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((target, port)) == 0:
            open_ports.append(port)
        s.close()
    return open_ports