from dataclasses import dataclass
from typing import Dict, Optional, Any, List
import json
import os

@dataclass
class FieldDefinition:
    offset: int
    length: int
    description: str


@dataclass
class ProtocolDefinition:
    name: str
    fields: Dict[str, FieldDefinition]
    next_protocol: Optional[Dict[str, Any]] = None


class ProtocolParser:
    def __init__(self, payload: bytes, structure_file: str, base_offset: int = 0):
        self.payload = payload
        self.structure_file = structure_file
        self.base_offset = base_offset
        self.protocol = self._load_protocol(structure_file)
        self._parsed_values: Dict[str, int] = {}

    def _load_protocol(self, structure_file: str) -> ProtocolDefinition:
        with open(structure_file, 'r') as f:
            data = json.load(f)

        fields = {}
        for field_name, field_data in data["header"].items():
            fields[field_name] = FieldDefinition(
                offset=field_data["offset"],
                length=field_data["length"],
                description=field_data["description"]
            )

        return ProtocolDefinition(
            name=data["name"],
            fields=fields,
            next_protocol=data.get("next_protocol")
        )

    def _extract_bits(self, start_bit: int, num_bits: int) -> int:
        absolute_start = start_bit + (self.base_offset * 8)
        start_byte = absolute_start // 8
        bit_offset = absolute_start % 8
        num_bytes = (bit_offset + num_bits + 7) // 8

        if start_byte + num_bytes > len(self.payload):
            return 0

        bytes_data = self.payload[start_byte:start_byte + num_bytes]
        value = int.from_bytes(bytes_data, byteorder='big')
        right_shift = (8 * num_bytes) - (bit_offset + num_bits)
        value = (value >> right_shift)
        mask = (1 << num_bits) - 1
        return value & mask

    def _evaluate_expression(self, expression: str) -> int:
        expression = expression.strip()
        if not expression.startswith("calculate:"):
            return int(expression)

        calc = expression[10:].strip()
        return eval(calc, {}, self._parsed_values)

    def _get_next_protocol_parser(self) -> Optional['ProtocolParser']:
        if not self.protocol.next_protocol:
            return None

        next_proto = self.protocol.next_protocol
        start_after = self._evaluate_expression(next_proto["start_after"])

        current_dir = os.path.dirname(os.path.abspath(self.structure_file))

        if "file" in next_proto:
            next_file = os.path.join(current_dir, next_proto["file"])
            return ProtocolParser(self.payload, next_file, start_after)

        if "selector" in next_proto:
            selector_value = self._parsed_values[next_proto["selector"]]
            if str(selector_value) in next_proto["mappings"]:
                file_path = os.path.join(current_dir,
                                         next_proto["mappings"][str(selector_value)]["file"])
                return ProtocolParser(self.payload, file_path, start_after)

        return None

    def parse(self) -> Dict[str, Dict[str, Any]]:
        result = {self.protocol.name: {}}

        # Parse current protocol
        for field_name, field_def in self.protocol.fields.items():
            value = self._extract_bits(field_def.offset, field_def.length)
            self._parsed_values[field_name] = value
            result[self.protocol.name][field_name] = {
                "value": value,
                "description": field_def.description
            }

        # Parse next protocol if exists
        next_parser = self._get_next_protocol_parser()
        if next_parser:
            next_result = next_parser.parse()
            result.update(next_result)

        return result

    def get_field_value(self, field_name: str) -> Optional[int]:
        if field_name not in self.protocol.fields:
            return None
        field = self.protocol.fields[field_name]
        return self._extract_bits(field.offset, field.length)