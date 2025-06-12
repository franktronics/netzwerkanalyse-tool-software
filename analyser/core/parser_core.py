from .services import ParserService
from .models import ProtocolDefinition, FieldDefinition
from ..ports import FileManagerPort
from typing import Type

class ParserCore:
    def __init__(self, file_manager_adapter: Type[FileManagerPort]):
        # Ports
        self.file_manager = file_manager_adapter()

        # Services and Models
        self._parser_service = ParserService()

        # Logic
        self._entry_file = "protocols/config/ethernet.json"
        self._protocol_definitions: dict[str, ProtocolDefinition] = {}

    def _get_protocol_definition(self, file_name: str) -> ProtocolDefinition:
        """
        Load the protocol definition from a JSON file, caching it for future use.
        """
        if file_name in self._protocol_definitions:
            return self._protocol_definitions[file_name]

        file_data = self.file_manager.load_json_file(file_name)
        fields = {}
        for field_name, field_data in file_data["header"].items():
            fields[field_name] = FieldDefinition(
                offset=field_data["offset"],
                length=field_data["length"],
                description=field_data["description"]
            )

        protocol = ProtocolDefinition(
            name=file_data["name"],
            fields=fields,
            next_protocol=file_data.get("next_protocol")
        )
        self._protocol_definitions[file_name] = protocol
        return protocol

    def parse_one_packet(self, packet: bytes) -> dict[str, dict[str, any]]:
        self._parser_service.clear()
        entry_protocol = self._get_protocol_definition(self._entry_file)

        result = {}
        src_mac, dest_mac = self._parser_service.get_mac_adress(packet)
        result["mac"] = {
            "src": src_mac,
            "dst": dest_mac
        }

        result.update(self._parser_service.parse_one_protocol(packet, entry_protocol, 0))
        next_file, start_after = self._parser_service.get_next_protocol_data(entry_protocol, self._entry_file)

        while next_file is not None:
            self._parser_service.clear()
            next_protocol = self._get_protocol_definition(next_file)
            result.update(self._parser_service.parse_one_protocol(packet, next_protocol, start_after))

            next_file, start_after = self._parser_service.get_next_protocol_data(next_protocol, self._entry_file)

        return result

    def parse_packets_list(self, packets: list[bytes]) -> list[dict[str, dict[str, any]]]:
        result = []
        for packet in packets:
            result.append(self.parse_one_packet(packet))
        return result

    def set_entry_file(self, entry_file: str) -> None:
        """
        Set the entry file for the parser core, clearing any cached protocol definitions.
        """
        self._entry_file = entry_file
        self._protocol_definitions.clear()