#!/usr/bin/env python3
import socket
import struct
import textwrap
import time
from datetime import datetime


def main():
    # Create a data link level socket with PF_PACKET
    # PF_PACKET : data link layer
    # ntohs(0x0800) : IP protocol
    # ntohs(0x0806) : ARP protocol
    # ntohs(0x86DD) : IPv6 protocol
    # ntohs(0x8035) : RARP protocol
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

    print("=== IP Communications Tracker ===")
    print("Press Ctrl+C to stop capturing\n")

    try:
        while True:
            raw_data, addr = conn.recvfrom(65536)
            dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)

            # Check if it's an IP packet (0x0800)
            if eth_proto == 8:
                version, header_length, ttl, proto, src, target, data = ipv4_packet(data)

                # Get current time for timestamp
                timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]

                print(f"\n[{timestamp}] IP Communication detected:")
                print(f"Ethernet: {src_mac} -> {dest_mac}, Proto: {eth_proto}")
                print(f"IPv{version}: {src} -> {target}, TTL: {ttl}")

                # Layer 4 protocol analysis
                if proto == 1:  # ICMP
                    icmp_type, code, checksum, data = icmp_packet(data)
                    print(f"ICMP: Type: {icmp_type}, Code: {code}, Checksum: {checksum}")

                elif proto == 6:  # TCP
                    src_port, dest_port, sequence, acknowledgment, flags, data = tcp_packet(data)
                    print(f"TCP: {src}:{src_port} -> {target}:{dest_port}")
                    print(f"     Sequence: {sequence}, Acknowledgment: {acknowledgment}")
                    print(f"     Flags: {parse_tcp_flags(flags)}")

                    if data:
                        if len(data) > 100:
                            print(f"     Data: {len(data)} bytes")
                            print(format_multi_line("\t\t", data[:100]) + "...")
                        else:
                            print(f"     Data: {len(data)} bytes")
                            print(format_multi_line("\t\t", data))

                elif proto == 17:  # UDP
                    src_port, dest_port, length, data = udp_packet(data)
                    print(f"UDP: {src}:{src_port} -> {target}:{dest_port}, Length: {length}")

                    if data:
                        if len(data) > 100:
                            print(f"     Data: {len(data)} bytes")
                            print(format_multi_line("\t\t", data[:100]) + "...")
                        else:
                            print(f"     Data: {len(data)} bytes")
                            print(format_multi_line("\t\t", data))

                else:
                    print(f"Other protocol: {proto}")
                    if data:
                        if len(data) > 100:
                            print(f"     Data: {len(data)} bytes")
                            print(format_multi_line("\t\t", data[:100]) + "...")
                        else:
                            print(f"     Data: {len(data)} bytes")
                            print(format_multi_line("\t\t", data))

                print("-" * 80)  # Separator line for better readability

    except KeyboardInterrupt:
        print("\nCapture terminated.")
    except PermissionError:
        print("\nError: Insufficient privileges. Run this script with administrator rights (sudo).")
    except Exception as e:
        print(f"\nError: {e}")


# Ethernet frame parsing
def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.ntohs(proto), data[14:]


# Format MAC address (e.g., AA:BB:CC:DD:EE:FF)
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()


# IPv4 packet parsing
def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]


# Convert IPv4 address from bytes to string
def ipv4(addr):
    return '.'.join(map(str, addr))


# ICMP packet parsing
def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:]


# TCP packet parsing
def tcp_packet(data):
    src_port, dest_port, sequence, acknowledgment, offset_reserved_flags = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flags = offset_reserved_flags & 0x1FF
    return src_port, dest_port, sequence, acknowledgment, flags, data[offset:]


# Translate TCP flags to make them readable
def parse_tcp_flags(flags):
    flag_names = []
    if flags & 0x001:  # FIN
        flag_names.append("FIN")
    if flags & 0x002:  # SYN
        flag_names.append("SYN")
    if flags & 0x004:  # RST
        flag_names.append("RST")
    if flags & 0x008:  # PSH
        flag_names.append("PSH")
    if flags & 0x010:  # ACK
        flag_names.append("ACK")
    if flags & 0x020:  # URG
        flag_names.append("URG")
    if flags & 0x040:  # ECE
        flag_names.append("ECE")
    if flags & 0x080:  # CWR
        flag_names.append("CWR")
    if flags & 0x100:  # NS
        flag_names.append("NS")

    if not flag_names:
        return "None"

    return ", ".join(flag_names)


# UDP packet parsing
def udp_packet(data):
    src_port, dest_port, length = struct.unpack('! H H H 2x', data[:8])
    return src_port, dest_port, length, data[8:]


# Format multi-line data
def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])


if __name__ == "__main__":
    main()