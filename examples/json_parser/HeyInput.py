import json
import os

def load_packet(packet_path):
    # Lädt ein Hex-Paket aus einer Datei, entfernt Leerzeichen und wandelt es in einen Bit-String um
    with open(packet_path, "r") as file:
        hex_string = file.read().strip().replace(" ", "")
    packet = ''.join(f'{int(hex_string[i:i+2], 16):08b}' for i in range(0, len(hex_string), 2))
    print(f"\nHex-Daten: {hex_string}")
    print(f"Binärdaten: {packet}")
    return packet

def load_structure(json_file):
    # Lädt die Protokollstruktur aus einer JSON-Datei
    with open(json_file, "r") as file:
        return json.load(file)

def evaluate_expression(expression, parsed_fields):
    # Bewertet eine Ausdrucksform (z. B. "calculate: header_length * 4") basierend auf bereits geparsten Feldern
    if not expression.startswith("calculate:"):
        return int(expression)
    expr = expression.replace("calculate:", "").strip()
    return eval(expr, {}, parsed_fields)

def format_by_type(type_name, bit_string, types_definitions):
    # Formatiert einen Bit-String entsprechend der Typdefinition aus type.json

    # Falls kein definierter Typ, Rückgabe als Ganzzahl
    if type_name not in types_definitions:
        return int(bit_string, 2)

    type_def = types_definitions[type_name]  # Typdefinition abrufen
    separator = type_def.get("Seperate", ".")  # Standard: Punkt als Trenner
    structure = type_def.get("Structure", {})  # Strukturdefinition abrufen
    vision = type_def.get("Vison", "def")  # Standard: Punkt als Trenner
    parts = []
    
    for _, field in structure.items():
        offset = field["offset"]
        length = field["length"]
        part_bits = bit_string[offset:offset + length]
        if vision == "dec":
            parts.append(str(int(part_bits, 2)))
        elif vision == "hex":
            parts.append(f"{int(part_bits, 2):x}")
        
    return separator.join(parts)

def analyze_packet(packet, structure_data, type_definitions, base_offset=0):
    # Analysiert ein Netzwerkpaket gemäß der geladenen Protokollstruktur
    field_structure = structure_data["header"]
    protocol_name = structure_data["name"]

    print(f"\n--- {protocol_name} ---")
    result = {}
    parsed_fields = {}

    for field, attributes in field_structure.items():
        offset = base_offset * 8 + attributes["offset"]
        length = attributes["length"]
        bin_str = packet[offset:offset + length]

        # Prüfen, ob ein spezifischer Typ definiert ist
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

        print(f"{field}: {value} (Binär: {bin_str}) – {attributes.get('description', '')}")

    # Falls ein Folgeprotokoll definiert ist, rekursiv weitermachen
    if "next_protocol" in structure_data:
        selector = structure_data["next_protocol"]["selector"]
        mappings = structure_data["next_protocol"]["mappings"]
        start_after = evaluate_expression(structure_data["next_protocol"]["start_after"], parsed_fields)

        proto_value = parsed_fields[selector]
        if str(proto_value) in mappings:
            next_file = mappings[str(proto_value)]["file"]
            next_path = os.path.join(os.path.dirname(__file__), next_file)
            next_structure = load_structure(next_path)
            result["next_protocol"] = analyze_packet(packet, next_structure, type_definitions, base_offset=start_after)

    return result

# === Hauptprogramm ===
packet_bits=load_packet("paketHex.txt")
ipv4_structure = load_structure("ether.json")        # Lädt die Hauptstruktur (z. B. IPv4)
type_definitions = load_structure("type.json")      # Lädt die Typendefinitionen (z. B. ip4, etc.)

result = analyze_packet(packet_bits, ipv4_structure, type_definitions)
