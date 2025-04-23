import json
import os

def load_packet(packet_path):
    with open(packet_path, "r") as file:
        hex_string = file.read().strip().replace(" ", "")
    packet = ''.join(f'{int(hex_string[i:i+2], 16):08b}' for i in range(0, len(hex_string), 2))
    print(f"\nHex Data: {hex_string}")
    print(f"Binary Data: {packet}")
    return packet

def load_structure(json_file):
    with open(json_file, "r") as file:
        return json.load(file)

def evaluate_expression(expression, parsed_fields):
    if not expression.startswith("calculate:"):
        return int(expression)
    expr = expression.replace("calculate:", "").strip()
    return eval(expr, {}, parsed_fields)

def format_by_type(type_name, bit_string, types_definitions):
    """Entsprechend des type.json formatieren eines Bitstrings"""
    if type_name not in types_definitions:
        return int(bit_string, 2)  #wenn kein Type angegeben, dann zurück als "rohwert"

    if type_name == "ip4":
        ip_parts = []
        struktur = types_definitions["ip4"]["Struktur"]
        for _, feld in struktur.items():
            offset = feld["offset"]
            length = feld["length"]
            part = bit_string[offset:offset+length]
            ip_parts.append(str(int(part, 2)))
        return ".".join(ip_parts)

    # Erweiterbar für weitere Types
    return bit_string  #backup rückgabe "rohwert"

def analyze_packet(packet, structure_data, base_offset=0, type_def_path="type.json"):
    
    field_structure = structure_data["header"]
    protocol_name = structure_data["name"]

    # Load type definitions (ip4, etc.)
    type_definitions = load_structure(type_def_path)

    print(f"\n--- {protocol_name} ---")
    result = {}
    parsed_fields = {}

    for field, attributes in field_structure.items():
        offset = base_offset * 8 + attributes["offset"]
        length = attributes["length"]
        bin_str = packet[offset:offset + length]

        if "type" in attributes and attributes["type"]:
            value = format_by_type(attributes["type"], bin_str, type_definitions)
        else:
            value = int(bin_str, 2)

        parsed_fields[field] = value
        result[field] = {
            "value": value,
            "binary": bin_str,
            "description": attributes.get("description", "")
        }
        print(f"{field}: {value} (Binary: {bin_str}) – {attributes.get('description', '')}")

    # Folgende Protokolle
    if "next_protocol" in structure_data:
        selector = structure_data["next_protocol"]["selector"]
        mappings = structure_data["next_protocol"]["mappings"]
        start_after = evaluate_expression(structure_data["next_protocol"]["start_after"], parsed_fields)

        proto_value = parsed_fields[selector]
        if str(proto_value) in mappings:
            next_file = mappings[str(proto_value)]["file"]
            next_path = os.path.join(os.path.dirname(json_path), next_file)
            result["next_protocol"] = analyze_packet(packet, next_path, base_offset=start_after, type_def_path=type_def_path)

    return result

# === Main ===
packet_bits = load_packet("paketHex.txt")
structure_data = load_structure("ipv4.json")
result = analyze_packet(packet_bits, structure_data)
