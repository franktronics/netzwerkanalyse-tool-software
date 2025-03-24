import model

def start_sniffer():
    """Ruft die Sniffer-Funktion aus dem Model auf und gibt die Pakete zurück."""
    return model.sniff_packets()
