import json

def lade_paket():
    """Lädt das Paket und wandelt den Hex-String in Binärdaten um."""
    with open("paket.txt", "r") as file:
        hex_data = file.read().strip().replace(" ", "")
    
    # Hex-String zu Bytes umwandeln
    byte_data = bytes.fromhex(hex_data)

    # Umwandlung der Bytes in eine Liste von Bits für die spätere Analyse
    paket = ''.join(f'{byte:08b}' for byte in byte_data)

    print(f"Byte-Daten: {byte_data}")
    print(f"Hex-Daten: {hex_data}")
    print(f"Binärdaten (Bits): {paket}")
    return paket

def load_ipv4_structure(json_file):
    #Lädt die IPv4-Header-Struktur aus einer JSON-Datei.
    with open(json_file, "r") as file:
        JASON=json.load(file)
        print(JASON)
        return JASON
    

def extract_field(data, offset, length):
    #Extrahiert ein Feld aus den binären Daten anhand des Offsets und der Bitlänge.
    Erg=1

    return Erg

def analyse_ipv4_paket(paket, structure):
    #Analysiert ein IPv4-Paket basierend auf der JSON-Beschreibung.
    result = {}
    print("\nPaket Analyse:")
    
   
    return result

# Hauptprogramm
paket = lade_paket()
ipv4_struktur = load_ipv4_structure("IPv4.json") 
analysis = analyse_ipv4_paket(paket, ipv4_struktur)
