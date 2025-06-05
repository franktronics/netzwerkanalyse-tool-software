from typing import Dict, ClassVar, Tuple
import os
from utils.functions import TypeConverter
from ..models import ParserModel, ProtocolDefinition


class ParserService(ParserModel):
    _protocol_cache: ClassVar[Dict[str, ProtocolDefinition]] = {}

    def __init__(self):
        super().__init__()
        self._parsed_values: Dict[str, int] = {}
        #self._converter = TypeConverter(type_file='protocols/config/types.json')

    def get_next_protocol_data(
            self,
            actual_protocol_def: ProtocolDefinition,
            entry_file: str
        ) -> Tuple[str, int] | Tuple[None, 0]:

        if not actual_protocol_def.next_protocol:
            return None, 0

        next_proto = actual_protocol_def.next_protocol
        start_after = self.evaluate_expression(next_proto["start_after"], self._parsed_values)

        current_dir = os.path.dirname(os.path.abspath(entry_file))

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

    def parse_one_protocol(
            self,
            raw_data: bytes,
            protocol_def: ProtocolDefinition,
            base_offset: int = 0,
        ) -> dict[str, dict[str, any]]:

        result = {protocol_def.name: {}}

        for field_name, field_def in protocol_def.fields.items():
            value = self.extract_bits(raw_data, field_def.offset, field_def.length, base_offset)
            self._parsed_values[field_name] = value

            result[protocol_def.name][field_name] = {
                "value": value,
                "description": field_def.description
            }

        return result

    def clear(self) -> None:
        """
        Clear the internal state of the parser service.
        """
        self._parsed_values.clear()