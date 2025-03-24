import socket
import struct

def get_protocol_name(protocol_num):
    """Übersetzt die Protokollnummer in einen lesbaren Namen."""
    protocol_dict = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
    }
    return protocol_dict.get(protocol_num, f"Unbekannt ({protocol_num})")

def sniff_packets():
    """Sniffet 10 Pakete und gibt eine Liste von Tupeln (Protokoll, Rohdaten) zurück."""
    packet_list = []
    
    # RAW-Socket für Ethernet-Frames öffnen (nur Linux)
    sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    try:
        for _ in range(10):  # 10 Pakete sammeln
            raw_data, _ = sniffer.recvfrom(65565)

            # Ethernet-Frame Header extrahieren (erste 14 Bytes)
            eth_header = raw_data[:14]
            eth = struct.unpack("!6s6sH", eth_header)
            eth_protocol = socket.ntohs(eth[2])  # Protokolltyp

            # Falls es sich um ein IPv4-Paket handelt
            if eth_protocol == 0x0800:
                ip_header = raw_data[14:34]  # IP-Header extrahieren (20 Bytes)
                iph = struct.unpack("!BBHHHBBH4s4s", ip_header)
                protocol = iph[6]  # Protokollnummer
                protocol_name = get_protocol_name(protocol)
            else:
                protocol_name = f"Nicht-IP (EtherType: {hex(eth_protocol)})"

            packet_list.append((protocol_name, raw_data))

    finally:
        sniffer.close()

    return packet_list
