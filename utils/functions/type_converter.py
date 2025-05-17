import json
from typing import Any, Dict, List

class TypeConverter:
    def __init__(self, type_file: str = "types.json"):
        self.type_file = type_file
        self.types = self._load_types()

    def _load_types(self) -> Dict:
        """Load types from JSON file"""
        with open(self.type_file, 'r') as f:
            return json.load(f)

    def convert(self, value: int, type_name: str) -> Any:
        """Convert a decimal value to specified type"""
        if type_name not in self.types["types"]:
            raise ValueError(f"Type {type_name} not defined")

        type_info = self.types["types"][type_name]
        result = value

        for step in type_info["steps"]:
            result = self._execute_step(result, step)

        return result

    def _execute_step(self, value: Any, step: Dict) -> Any:
        """Execute a single conversion step"""
        operation = step["operation"]

        if operation == "split":
            if "bits" in step:
                # Split based on bits
                parts = [(value >> i) & step["mask"] for i in step["bits"]]
                if step.get("format") == "hex":
                    parts = [format(p, f'0{step["padding"]}x') for p in parts]
                return parts
            elif "bytes" in step:
                # Split into bytes
                return [format((value >> i) & 0xFF, f'0{step["padding"]}x')
                        for i in range(0, value.bit_length(), 8)]

        elif operation == "join":
            return step["separator"].join(map(str, value))

        elif operation == "format":
            if step["base"] == 2:
                return format(value, '#b')
            elif step["base"] == 16:
                return format(value, '#x')
            return format(value, str(step["base"]))

        return value

    def add_type(self, name: str, type_info: Dict):
        """Add a new type to the JSON file"""
        self.types["types"][name] = type_info
        self._save_types()

    def _save_types(self):
        """Save types to JSON file"""
        with open(self.type_file, 'w') as f:
            json.dump(self.types, f, indent=2)

    def list_types(self) -> List[str]:
        """Return a list of available types"""
        return list(self.types["types"].keys())

    def get_type_info(self, type_name: str) -> Dict:
        """Get information about a specific type"""
        if type_name not in self.types["types"]:
            raise ValueError(f"Type {type_name} not defined")
        return self.types["types"][type_name]