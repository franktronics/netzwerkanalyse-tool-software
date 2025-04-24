from dataclasses import dataclass
from typing import Dict, Optional, Any, ClassVar, Tuple
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
    _protocol_cache: ClassVar[Dict[str, ProtocolDefinition]] = {}

    def __init__(self, entry_file: str):
        self._base_file = entry_file
        self._entry_file = entry_file
        self._actual_protocol = None
        self._parsed_values: Dict[str, int] = {}

    def _load_protocol(self, structure_file: str) -> ProtocolDefinition:
        abs_path = os.path.abspath(structure_file)

        # Return cached protocol if available
        if abs_path in self._protocol_cache:
            return self._protocol_cache[abs_path]

        with open(structure_file, 'r') as f:
            data = json.load(f)

        fields = {}
        for field_name, field_data in data["header"].items():
            fields[field_name] = FieldDefinition(
                offset=field_data["offset"],
                length=field_data["length"],
                description=field_data["description"]
            )

        protocol = ProtocolDefinition(
            name=data["name"],
            fields=fields,
            next_protocol=data.get("next_protocol")
        )

        # Cache the protocol definition
        self._protocol_cache[abs_path] = protocol
        return protocol

    def _extract_bits(self, raw_data: bytes, start_bit: int, num_bits: int, base_offset: int = 0) -> int:
        absolute_start = start_bit + base_offset
        start_byte = absolute_start // 8
        bit_offset = absolute_start % 8
        num_bytes = (bit_offset + num_bits + 7) // 8

        if start_byte + num_bytes > len(raw_data):
            return 0

        bytes_data = raw_data[start_byte:start_byte + num_bytes]
        value = int.from_bytes(bytes_data, byteorder='big')
        right_shift = (8 * num_bytes) - (bit_offset + num_bits)
        value = (value >> right_shift)
        mask = (1 << num_bits) - 1
        return value & mask

    def _evaluate_expression(self, expression: str | int) -> int:
        if isinstance(expression, int):
            return expression
        if not isinstance(expression, str):
            raise ValueError("Expression must be a string or an integer.")

        expression = expression.strip()
        if not expression.startswith("calculate:"):
            return int(expression)

        calc = expression[10:].strip()
        return eval(calc, {}, self._parsed_values)

    def _get_next_protocol_data(self) -> Tuple[str, int] | Tuple[None, 0]:
        if not self._actual_protocol.next_protocol:
            return None, 0

        next_proto = self._actual_protocol.next_protocol
        start_after = self._evaluate_expression(next_proto["start_after"])

        current_dir = os.path.dirname(os.path.abspath(self._entry_file))

        next_file = None
        if "file" in next_proto:
            next_file = os.path.join(current_dir, next_proto["file"])
        elif "selector" in next_proto:
            selector_value = str(self._parsed_values[next_proto["selector"]])
            if selector_value in next_proto["mappings"]:
                next_file = os.path.join(current_dir, next_proto["mappings"][str(selector_value)]["file"])
            else:
                raise ValueError(f"Selector value '{selector_value}' not found in mappings.")

        return next_file, start_after

    def _parse_one_protocol(self, raw_data: bytes, base_offset: int = 0) -> Dict[str, Dict[str, Any]]:
        result = {self._actual_protocol.name: {}}

        for field_name, field_def in self._actual_protocol.fields.items():
            value = self._extract_bits(raw_data, field_def.offset, field_def.length, base_offset)
            self._parsed_values[field_name] = value
            result[self._actual_protocol.name][field_name] = {
                "value": value,
                "description": field_def.description
            }

        return result

    def _get_mac_adress(self, raw_data: bytes) -> Tuple[str, str]:
        """
        get source and destination mac address from raw data
        this will be used as primary key for the packet in the database
        so we can search for a specific packet knowning the mac address
        """
        dst_mac = raw_data[0:6].hex()
        src_mac = raw_data[6:12].hex()
        dst_mac = ":".join(dst_mac[i:i + 2] for i in range(0, len(dst_mac), 2))
        src_mac = ":".join(src_mac[i:i + 2] for i in range(0, len(src_mac), 2))
        return src_mac, dst_mac

    def parse(self, raw_data: bytes) -> Dict[str, Dict[str, Any]]:
        self._entry_file = self._base_file
        self._parsed_values.clear()
        self._actual_protocol = self._load_protocol(self._entry_file)

        result = {}

        src_mac, dest_mac = self._get_mac_adress(raw_data)
        result["mac"] = {
            "src": src_mac,
            "dst": dest_mac
        }

        result.update(self._parse_one_protocol(raw_data))
        next_file, start_after = self._get_next_protocol_data()

        while next_file is not None:
            self._entry_file = next_file
            self._parsed_values.clear()
            self._actual_protocol = self._load_protocol(next_file)
            result.update(self._parse_one_protocol(raw_data = raw_data, base_offset = start_after))

            next_file, start_after = self._get_next_protocol_data()

        return result