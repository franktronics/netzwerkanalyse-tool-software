import json
from typing import Dict, Any, Optional
import ipaddress


class PayloadParser:
    def __init__(self, payload: bytes, structure_file: str):
        self.payload = payload
        with open(structure_file, 'r') as f:
            self.structure = json.load(f)

        # Create section objects dynamically
        for section_name, section_data in self.structure.items():
            setattr(self, section_name, _Section(section_name))

        self.parsed = False

    def _extract_bits(self, start_bit: int, num_bits: int) -> int:
        """
        Extract bits from payload

        Args:
            start_bit: Starting bit position (0-indexed)
            num_bits: Number of bits to extract

        Returns:
            Extracted value as integer
        """
        # Calculate start byte and bit within that byte
        start_byte = start_bit // 8
        bit_offset = start_bit % 8

        # Calculate how many bytes we need to read
        num_bytes = (bit_offset + num_bits + 7) // 8

        # Ensure we don't read beyond the payload
        if start_byte + num_bytes > len(self.payload):
            return 0

        # Extract the bytes
        bytes_data = self.payload[start_byte:start_byte + num_bytes]

        # Convert bytes to integer (big endian)
        value = int.from_bytes(bytes_data, byteorder='big')

        # Calculate bit mask and shift
        # We need to shift right to remove trailing bits we don't want
        right_shift = (8 * num_bytes) - (bit_offset + num_bits)
        value = (value >> right_shift)

        # Create mask to extract only the bits we want
        mask = (1 << num_bits) - 1
        value = value & mask

        return value

    def _format_value(self, value: int, type_name: Optional[str], property_info: Dict) -> Any:
        """
        Format extracted value based on type

        Args:
            value: Raw integer value
            type_name: Type of formatting to apply (e.g., 'ip')
            property_info: Property information dictionary

        Returns:
            Formatted value
        """
        if type_name == "ip":
            # Convert 32-bit value to IP address string
            return str(ipaddress.IPv4Address(value))
        return value

    def parse(self) -> Dict[str, Any]:
        """
        Parse the payload according to the structure definition

        Returns:
            Dictionary containing parsed data
        """
        if self.parsed:
            return self.get_info()

        # First, parse all sections
        for section_name, section_properties in self.structure.items():
            section_obj = getattr(self, section_name)

            # Parse each property in the section
            for prop_name, prop_info in section_properties.items():
                # Extract bits for this property
                offset = prop_info.get("offset", 0)
                length = prop_info.get("length", 8)

                raw_value = self._extract_bits(offset, length)

                # Format the value if needed
                type_name = prop_info.get("type", None)
                value = self._format_value(raw_value, type_name, prop_info)

                # Create property object and add to section
                prop_obj = _Property(prop_name, value, prop_info)
                setattr(section_obj, prop_name, prop_obj)

        # Now handle conditional properties
        for section_name, section_properties in self.structure.items():
            section_obj = getattr(self, section_name)

            # Check conditions for each property
            for prop_name, prop_info in section_properties.items():
                prop_obj = getattr(section_obj, prop_name)

                # Evaluate condition if present
                condition = prop_info.get("condition", "True")
                try:
                    condition_result = eval(condition, {"self": self})
                    prop_obj.visible = bool(condition_result)
                except Exception as e:
                    prop_obj.visible = False
                    prop_obj.error = str(e)

        self.parsed = True
        return self.get_info()

    def get_info(self, detailed: bool = True) -> Dict[str, Any]:
        """
        Get structured information from the parsed payload

        Args:
            detailed: If True, return full property information with original JSON structure.
                     If False, return only the property values.

        Returns:
            Dictionary containing structured data from payload
        """
        if not self.parsed:
            self.parse()

        result = {}

        # Create result dictionary with the same structure as input
        for section_name in self.structure.keys():
            section_obj = getattr(self, section_name)
            section_dict = {}

            # Add each visible property
            for prop_name in self.structure[section_name].keys():
                prop_obj = getattr(section_obj, prop_name)

                if prop_obj.visible:
                    if detailed:
                        # Include all properties from the JSON structure plus the value
                        prop_dict = {
                            "value": prop_obj.value,
                            **{k: v for k, v in self.structure[section_name][prop_name].items()}
                        }
                        section_dict[prop_name] = prop_dict
                    else:
                        # Include only the value
                        section_dict[prop_name] = prop_obj.value

            if section_dict:  # Only add non-empty sections
                result[section_name] = section_dict

        return result


class _Section:
    """Helper class to represent a section of a packet"""

    def __init__(self, name: str):
        self.name = name


class _Property:
    """Helper class to represent a property of a packet section"""

    def __init__(self, name: str, value: Any, info: Dict):
        self.name = name
        self.value = value
        self.info = info
        self.visible = True
        self.error = None