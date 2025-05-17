from dataclasses import dataclass
from typing import Dict, Optional, Any, Tuple

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

@dataclass
class ParserModel:
    def extract_bits(self, raw_data: bytes, start_bit: int, num_bits: int, base_offset: int = 0) -> int:
        """
        Extract a specific number of bits from raw data starting from a given bit position.
        """
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

    def evaluate_expression(self, expression: str | int, context) -> int:
        """
        Evaluate a mathematical expression or return an integer.
        """
        if isinstance(expression, int):
            return expression
        if not isinstance(expression, str):
            raise ValueError("Expression must be a string or an integer.")

        expression = expression.strip()
        if not expression.startswith("calculate:"):
            return int(expression)

        calc = expression[10:].strip()
        return eval(calc, {}, context)

    def get_mac_adress(self, raw_data: bytes) -> Tuple[str, str]:
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