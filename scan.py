import port_scanner

ziel = input("Ziel: ")
von = int(input("Von Port: "))
bis = int(input("Bis Port: "))
print(port_scanner.get_open_ports(ziel, [von, bis], True))