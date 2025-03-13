import socket
import struct


def packet_sniffer():
    # Erstelle einen Raw-Socket
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

    # Binde den Socket an die lokale Schnittstelle
    host = socket.gethostbyname(socket.gethostname())
    sniffer.bind((host, 0))

    # Socket so konfigurieren, dass die IP-Header erhalten bleiben
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Aktiviert den Promiscuous-Modus (nur unter Windows erforderlich)
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        print("Packet Sniffing startet. Drücken Sie Strg+C zum Beenden.")
        while True:
            # Paket empfangen
            raw_data, _ = sniffer.recvfrom(65565)
            print(raw_data)

    except KeyboardInterrupt:
        print("\nPacket Sniffing gestoppt.")

    finally:
        # Deaktiviert den Promiscuous-Modus
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == "__main__":
    packet_sniffer()
