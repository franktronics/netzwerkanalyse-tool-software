from sockets import SocketInit
import time
from .protocol_parser import ProtocolParser
import json

class EthernetParser:
    def __init__(self, socket_obj: SocketInit):
        self.socket_obj = socket_obj
        self.run()
        self.timer = 0 #time in seconds

    def run(self):
        self.timer = time.time()
        while True:
            if time.time() - self.timer > 10:
                break
            raw_data, addr = self.socket_obj.receive()
            header_parsed, payload = self.parser(raw_data)
            print(raw_data)

            print(header_parsed)

            match header_parsed["ether_type"]:
                case '0800': # IPv4
                    payload_parser = ProtocolParser(payload, structure_file="protocols/config/ipv4.json")
                    payload_parsed = payload_parser.parse()
                    print(json.dumps(payload_parsed, indent=2, ensure_ascii=False))
                case '0806':  # ARP
                    payload_parser = ProtocolParser(payload, structure_file="protocols/config/arp.json")
                    payload_parsed = payload_parser.parse()
                    print(json.dumps(payload_parsed, indent=2, ensure_ascii=False))
                case _:
                    print("Ethernet type not supported")
            print("=====================================")

    # Raw packet structure
    # 1. Ethernet Header (14 bytes)
    #    - Destination MAC Address (6 bytes)
    #    - Source MAC Address (6 bytes)
    #    - EtherType (2 bytes)

    # 2. Payload (variable length)
    #    - Can be IP packet, ARP, etc.
    @classmethod
    def parser(cls, packet: bytes):
        dest_mac = packet[0:6]
        src_mac = packet[6:12]
        ether_type = packet[12:14]
        payload = packet[14:]

        return {
            'destination_mac': dest_mac.hex(':'),
            'source_mac': src_mac.hex(':'),
            'ether_type': ether_type.hex()
        }, payload
            
    def stop(self):
        self.socket_obj.close()
        print("Socket closed")