class IPV4Parser:
    def __init__(self, payload: bytes):
        self.payload = payload
        self.infos = {}

    def _parse_header(self):
        """
        Parse the IPv4 header details
        """
        version_ihl = self.payload[0]
        self.infos['version'] = version_ihl >> 4
        self.infos['header_length'] = (version_ihl & 0x0F) * 4

        self.infos['total_length'] = int.from_bytes(self.payload[2:4], byteorder='big')
        self.infos['protocol'] = self.payload[9]

        self.infos['source_ip'] = '.'.join(str(x) for x in self.payload[12:16])
        self.infos['destination_ip'] = '.'.join(str(x) for x in self.payload[16:20])

    def _parse_protocol_details(self):
        """
        Parse protocol-specific details
        """
        protocols = {
            1: 'ICMP',
            6: 'TCP',
            17: 'UDP'
        }

        header_length = self.infos['header_length']
        ip_payload = self.payload[header_length:]

        self.infos['protocol_name'] = protocols.get(self.infos['protocol'], 'Unknown')

        if self.infos['protocol'] == 1:  # ICMP
            self.infos['icmp_type'] = ip_payload[0]
            self.infos['icmp_code'] = ip_payload[1]
        elif self.infos['protocol'] in [6, 17]:  # TCP or UDP
            self.infos['source_port'] = int.from_bytes(ip_payload[0:2], byteorder='big')
            self.infos['destination_port'] = int.from_bytes(ip_payload[2:4], byteorder='big')

    def get_infos(self):
        """
        Extract and populate packet information
        """
        self._parse_header()
        self._parse_protocol_details()
        return self.infos

    @classmethod
    def parse(cls, payload: bytes):
        """
        Class method to parse payload and return infos
        """
        instance = cls(payload)
        return instance.get_infos()