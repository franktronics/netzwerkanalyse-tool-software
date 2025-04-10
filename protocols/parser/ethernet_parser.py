from sockets import SocketInit
from .protocol_parser import ProtocolParser
import json
from typing import Dict, Any

class EthernetParser:
    def __init__(self):
        self.header_parsed = None
        self.payload_parsed = None

    def run(self, raw_data) -> Dict[str, Any]:
        self.header_parsed = self.parse_header(raw_data)
        self.payload_parsed = self.parse_payload(raw_data)

        print(raw_data)
        print(json.dumps(self.header_parsed, indent=2, ensure_ascii=False))
        print(json.dumps(self.payload_parsed, indent=2, ensure_ascii=False))
        print("=====================================")

        merged_data = {
            "header": self.header_parsed,
            "payload": self.payload_parsed
        }
        return merged_data

    def parse_payload(self, packet: bytes):
        # 2. Payload (variable length)
        #    - Can be IP packet, ARP, etc.

        payload = packet[14:]
        match self.header_parsed["ether_type"]:
            case '0800':  # IPv4
                protocol_parser = ProtocolParser(payload, structure_file="protocols/config/ipv4.json")
                return protocol_parser.parse()
            case '0806':  # ARP
                protocol_parser = ProtocolParser(payload, structure_file="protocols/config/arp.json")
                return protocol_parser.parse()
            case _:
                print("Ethernet type not supported")

    def parse_header(self, packet: bytes):
        # 1. Ethernet Header (14 bytes)
        #    - Destination MAC Address (6 bytes)
        #    - Source MAC Address (6 bytes)
        #    - EtherType (2 bytes)

        dest_mac = packet[0:6]
        src_mac = packet[6:12]
        ether_type = packet[12:14]

        return {
            'destination_mac': dest_mac.hex(':'),
            'source_mac': src_mac.hex(':'),
            'ether_type': ether_type.hex()
        }