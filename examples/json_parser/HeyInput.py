import json

def load_packet(packet_path):
    with open(packet_path, "r") as file:
        hex_string = file.read().strip().replace(" ", "")  # Remove spaces if present

    # Convert hex string to binary string
    packet = ''.join(f'{int(hex_string[i:i+2], 16):08b}' for i in range(0, len(hex_string), 2))

    print(f"\nHex Data: {hex_string}")
    print(f"Binary Data: {packet}")
    return packet

def load_structure(json_file):
    # Load header structure from a JSON file
    with open(json_file, "r") as file:
        structure = json.load(file)
        return structure["header"]  # Return only the header section

def analyze_packet(packet, structure):
    # Analyze an IPv4 packet based on the JSON structure
    print("\nPacket Analysis:")
    result = {}
    for field, attributes in structure.items():
        offset = attributes["offset"]
        length = attributes["length"]
        bin_str = packet[offset:offset + length]
        value = int(bin_str, 2)
        result[field] = {
            "value": value,
            "binary": bin_str,
            "description": attributes.get("description", "")
        }
        print(f"{field}: {value} (Binary: {bin_str}) – {attributes.get('description', '')}")
    return result

# Main program
packet = load_packet("paketHex.txt")
ipv4_structure = load_structure("ipv4.json")
analysis = analyze_packet(packet, ipv4_structure)
