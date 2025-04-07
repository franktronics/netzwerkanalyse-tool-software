from protocols.parser import ProtocolParser
from protocols.parser import EthernetParser
import json

if __name__ == "__main__":
    ipv4_packet = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00E\x00\x00Cp\x7f@\x00@\x11\xcb\xf4\x7f\x00\x00\x01\x7f\x00\x005\xb3:\x005\x00/\xfevB7\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x06github\x03com\x00\x00A\x00\x01\x00\x00)\x04\xb0\x00\x00\x00\x00\x00\x00'
    arp_packet = b"\xff\xff\xff\xff\xff\xff\x08\x00'%\x83~\x08\x06\x00\x01\x08\x00\x06\x04\x00\x01\x08\x00'%\x83~\n\x00\x02\x0f\x00\x00\x00\x00\x00\x00\n\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    # Ethernet header
    ethernet_header, payload = EthernetParser.parser(ipv4_packet)
    # Ipv4
    parser = ProtocolParser(payload, "protocols/config/ipv4.json")
    result = parser.parse()

    # Print the parsed result
    print("Ethernet Header:")
    print(json.dumps(ethernet_header, indent=2, ensure_ascii=False))
    print("\nParsed IPV4 Payload:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("-----------ARP-----------")
    # Ethernet header
    ethernet_header, payload = EthernetParser.parser(arp_packet)
    # ARP
    parser = ProtocolParser(payload, "protocols/config/arp.json")
    result = parser.parse()
    # Print the parsed result

    print("Ethernet Header:")
    print(json.dumps(ethernet_header, indent=2, ensure_ascii=False))
    print("\nParsed ARP Payload:")
    print(json.dumps(result, indent=2, ensure_ascii=False))