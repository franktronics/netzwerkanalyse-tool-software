import json

def lade_paket(adresse_paket):
    with open(adresse_paket, "r") as file:
        hex_string = file.read().strip().replace(" ", "")  # Entfernt Leerzeichen, falls vorhanden

    # Umwandlung in Binärdaten
    paket = ''.join(f'{int(hex_string[i:i+2], 16):08b}' for i in range(0, len(hex_string), 2))

    print(f"\nHex-Daten: {hex_string}")
    print(f"Binärdaten: {paket}")
    return paket

def load_struktur(json_file):
    #Lädt die Header-Struktur aus einer JSON-Datei.
    with open(json_file, "r") as file:
        JASON=json.load(file)
        print(JASON)
        return JASON
    



def analyse_paket(paket, struktur):
    #Analysiert ein IPv4-Paket basierend auf der JSON-Beschreibung.
    result = {}
    print("\nPaket Analyse:")
    for section, fields in struktur.items():
        print(f"=== {section} ===")
        for field, attributes in fields.items():
            bin_str=paket[attributes['offset']:attributes['offset']+attributes['length']]
            zahl = int(bin_str, 2)
            if field!= "Source_IP" and field!="Destination_IP":
                print(f"{field}: {zahl} in Binär {bin_str}")
            elif field == "Source_IP" or field =="Destination_IP":
                ip_parts = [str(int(bin_str[i:i+8], 2)) for i in range(0, 32, 8)]
                ip_address = ".".join(ip_parts)
                print(f"{field}: {ip_address} in Binär {bin_str}")

    return result

# Hauptprogramm
paket = lade_paket("examples/json_parser/paketHex.txt")
ipv4_struktur = load_struktur("examples/json_parser/IPv4.json")
analysis = analyse_paket(paket, ipv4_struktur)
