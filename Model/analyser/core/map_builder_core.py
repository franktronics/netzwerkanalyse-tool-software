from dataclasses import dataclass
import uuid

@dataclass
class Participant:
    mac: str
    name: str
    recipients: list[str]
    def add_recipient(self, recipient_mac: str):
        if recipient_mac not in self.recipients:
            self.recipients.append(recipient_mac)

class MapBuilderCore:
    def __init__(self):
        self.mac_address = None
        self.default_pc_name = "MY COMPUTER"

    def build_map(self, packets: list[tuple[int, str, str, str, str, str]]) -> list[Participant]:
        participants = {}
        if self.mac_address is None:
            self.get_local_mac_address()

        for packet in packets:
            _, _, src_mac, dst_mac, _, _ = packet
            if src_mac not in participants:
                name = self.default_pc_name if self.mac_address == src_mac.lower() else ""
                elt = Participant(mac=src_mac, name=name, recipients=[])
                elt.add_recipient(dst_mac)
                participants[src_mac] = elt
            else:
                participants[src_mac].add_recipient(dst_mac)

            if dst_mac not in participants:
                name = self.default_pc_name if self.mac_address == dst_mac.lower() else ""
                participants[dst_mac] = Participant(mac=dst_mac, name=name, recipients=[])

        return list(participants.values())

    def get_local_mac_address(self) -> str:
        mac = uuid.getnode()
        mac_address = ':'.join(("%012x" % mac)[i:i + 2] for i in range(0, 12, 2))
        self.mac_address = mac_address
        return mac_address
