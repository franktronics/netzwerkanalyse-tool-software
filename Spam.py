import socket
import struct
import os


def enable_promiscuous_mode(sock):
    """Aktiviere Promiscuous-Modus für Windows."""
    if os.name == 'nt':
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)


def disable_promiscuous_mode(sock):
    """Deaktiviere Promiscuous-Modus für Windows."""
    if os.name == 'nt':
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


def parse_ipv4_header(data):
    """IPv4-Header parsen."""
    header = struct.unpack('!BBHHHBBH4s4s', data[:20])

    version_ihl = header[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0xF) * 4

    ttl = header[5]
    protocol = header[6]
    src_ip = socket.inet_ntoa(header[8])
    dest_ip = socket.inet_ntoa(header[9])

    return {
        'Version': version,
        'Header Length': ihl,
        'TTL': ttl,
        'Protocol': protocol,
        'Source IP': src_ip,
        'Destination IP': dest_ip
    }, data[ihl:]


def parse_tcp_header(data):
    """TCP-Header parsen."""
    header = struct.unpack('!HHLLBBHHH', data[:20])

    src_port = header[0]
    dest_port = header[1]
    sequence = header[2]
    acknowledgment = header[3]
    data_offset = (header[4] >> 4) * 4

    return {
        'Source Port': src_port,
        'Destination Port': dest_port,
        'Sequence Number': sequence,
        'Acknowledgment Number': acknowledgment,
        'Header Length': data_offset
    }, data[data_offset:]


def hexdump(data, length=16):
    """Hexdump der Payload-Daten."""
    result = []
    for i in range(0, len(data), length):
        chunk = data[i:i + length]
        hex_bytes = ' '.join(f'{b:02x}' for b in chunk)
        ascii_bytes = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        result.append(f'{i:04x}  {hex_bytes:<48}  {ascii_bytes}')
    return '\n'.join(result)


def packet_sniffer():
    if os.name == 'nt':
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    else:
        sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    host = socket.gethostbyname(socket.gethostname())

    if os.name == 'nt':
        sniffer.bind((host, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        enable_promiscuous_mode(sniffer)

    print("[+] Sniffing gestartet. Drücken Sie Strg+C zum Beenden.")

    try:
        while True:
            raw_data, _ = sniffer.recvfrom(65565)

            # IPv4-Header parsen
            ipv4_info, remaining_data = parse_ipv4_header(raw_data)
            print("[IPv4 Header]")
            for key, value in ipv4_info.items():
                print(f"{key}: {value}")

            # TCP-Header parsen (nur wenn Protokoll TCP ist)
            if ipv4_info['Protocol'] == 6:
                tcp_info, payload = parse_tcp_header(remaining_data)
                print("\n[TCP Header]")
                for key, value in tcp_info.items():
                    print(f"{key}: {value}")

                # Payload anzeigen
                print("\n[Payload]")
                print(hexdump(payload))

            print("=" * 80)

    except KeyboardInterrupt:
        print("\n[!] Sniffing gestoppt.")
    finally:
        if os.name == 'nt':
            disable_promiscuous_mode(sniffer)


if __name__ == "__main__":
    packet_sniffer()
