import socket
import struct
import sys
import os


def enable_promiscuous_mode(sock):
    """Aktiviere Promiscuous-Modus für Windows."""
    if os.name == 'nt':
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)


def disable_promiscuous_mode(sock):
    """Deaktiviere Promiscuous-Modus für Windows."""
    if os.name == 'nt':
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


def packet_sniffer():
    # Überprüfen, welches Betriebssystem genutzt wird
    if os.name == 'nt':
        # Windows: Raw-Socket für IPv4-Pakete
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    else:
        # Linux: Raw-Socket für Ethernet-Frames
        sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    # Lokale Schnittstelle auswählen
    host = socket.gethostbyname(socket.gethostname())

    # Für Windows: an die Schnittstelle binden
    if os.name == 'nt':
        sniffer.bind((host, 0))
        # IP-Header einschließen
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        # Promiscuous-Modus aktivieren
        enable_promiscuous_mode(sniffer)

    print("[+] Sniffing gestartet. Drücken Sie Strg+C zum Beenden.")

    try:
        while True:
            raw_data, _ = sniffer.recvfrom(65565)
            print(raw_data)
            print("=" * 50)
    except KeyboardInterrupt:
        print("\n[!] Sniffing gestoppt.")
    finally:
        # Promiscuous-Modus für Windows deaktivieren
        if os.name == 'nt':
            disable_promiscuous_mode(sniffer)


if __name__ == "__main__":
    packet_sniffer()
