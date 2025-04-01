import json

def lade_paket():
    """Lädt das Paket und wandelt den Hex-String in Binärdaten um."""
    with open("paketByte.txt", "r") as file:
        byte_data = file.read().strip()
    


    # Optional: Umwandlung der Bytes in eine Liste von Bits für die spätere Analyse
    paket = ''.join(f'{ord(byte):08b}' for byte in byte_data)


    print(f"Byte-Daten: {byte_data}")
    print(f"Binärdaten (Bits): {paket}")
    return paket  # Gib die Bytes zurück, nicht den Bit-String

def load_ipv4_structure(json_file):
    #Lädt die IPv4-Header-Struktur aus einer JSON-Datei.
    with open(json_file, "r") as file:
        JASON=json.load(file)
        print(JASON)
        return JASON
    

def extract_field(Daten, Offset, Laenge):
    #Extrahiert ein Feld aus den binären Daten anhand des Offsets und der Bitlänge.
    Erg=1

    return Erg

def analyse_ipv4_paket(paket, struktur):
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
paket = lade_paket()
ipv4_struktur = load_ipv4_structure("IPv4.json") 
analysis = analyse_ipv4_paket(paket, ipv4_struktur)
