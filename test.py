from utils.functions import nic_detection
from analyser import NetworkAnalyserPort, NetworkAnalyser
import json

if __name__ == "__main__":
    nics = nic_detection()
    print(f"Detected NICs: {nics}")
    selected_nic = input(f"Please select a NIC (example: {nics[0]}): ")

    analyser: NetworkAnalyserPort = NetworkAnalyser()
    try:
        analyser.record(selected_nic)
        import time
        time.sleep(10)
        analyser.stop_record()

    except KeyboardInterrupt:
        analyser.stop_record()

    anylysis = analyser.database.get_all_analyses()
    print("### Analyses ###")
    print(json.dumps(anylysis, indent=4))

    selected_analysis = input("Please select an analysis id: ")
    packets = analyser.database.get_packets_by_analysis_id(selected_analysis)
    print("### First 10 Packets ###")
    for packet in packets[:10]:
        print(f"Packet ID: {packet[0]}, Timestamp: {packet[1]}, Src MAC: {packet[2]}, Dst MAC: {packet[3]}")

    selected_packet = input("Please select a packet id: ")
    # find packet where id matches selected_packet
    #packet = next((p for p in packets if p[4] == selected_packet), None)
    parsed_packet = analyser.parse_one_packet(packets[int(selected_packet)][4])
    print("### Parsed Packet ###")
    print(json.dumps(parsed_packet, indent=4))
