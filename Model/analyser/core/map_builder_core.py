from dataclasses import dataclass

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
        pass

    @classmethod
    def build_map(cls, packets: list[tuple[int, str, str, str, str, str]]) -> list[Participant]:
        participants = {}

        for packet in packets:
            _, _, src_mac, dst_mac, _, _ = packet
            if src_mac not in participants:
                elt = Participant(mac=src_mac, name="", recipients=[])
                elt.add_recipient(dst_mac)
                participants[src_mac] = elt
            else:
                participants[src_mac].add_recipient(dst_mac)

            if dst_mac not in participants:
                participants[dst_mac] = Participant(mac=dst_mac, name="", recipients=[])

        return list(participants.values())