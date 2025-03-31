import json

def lade_paket():
    """Lädt das Paket als Binärdaten (nicht als Hex-String)."""
    with open("paket.txt", "rb") as file:
        return file.read()

def load_ipv4_structure(json_file):
    """Lädt die IPv4-Header-Struktur aus einer JSON-Datei."""
    with open(json_file, "r") as file:
        return json.load(file)

def extract_field(data, offset, length):
    """Extrahiert ein Feld aus den binären Daten."""
    byte_offset = offset // 8
    bit_offset = offset % 8
    byte_length = (bit_offset + length + 7) // 8  # Rundet auf nächste volle Bytezahl auf

    field_bytes = data[byte_offset : byte_offset + byte_length]
    value = int.from_bytes(field_bytes, byteorder="big")

    if bit_offset > 0 or length % 8 != 0:
        value = (value >> (8 - ((bit_offset + length) % 8))) & ((1 << length) - 1)

    return value

def analyze_ipv4_paket(paket, structure):
    """Analysiert ein IPv4-Paket basierend auf der JSON-Beschreibung."""
    result = {}

    # IPv4-Header-Felder verarbeiten
    for field, details in structure["IPv4_Header"].items():
        value = extract_field(packet, details["offset"], details["length"])
        if field in ["Source_IP", "Destination_IP"]:
            value = ".".join(map(str, value.to_bytes(4, byteorder="big")))
        result[field] = value

    # UDP-Felder verarbeiten
    for field, details in structure["Transport_Layer"]["UDP"].items():
        value = extract_field(packet, details["offset"], details["length"])
        result[field] = value

    return result

# Laden der Daten
paket = lade_paket()
ipv4_structure = load_ipv4_structure("IPv4.json")
analysis = analyze_ipv4_packet(paket, ipv4_structure)

# Ergebnis ausgeben
for field, value in analysis.items():
    print(f"{field}: {value}")
