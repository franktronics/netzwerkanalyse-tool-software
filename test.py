from utils.functions import nic_detection
from analyser import NetworkAnalyser
import json

if __name__ == "__main__":
    nics = nic_detection()
    print(f"Detected NICs: {nics}")
    selected_nic = input(f"Please select a NIC (example: {nics[0]}): ")

    analyser = NetworkAnalyser()
    try:
        analyser.record(selected_nic)
        import time

        time.sleep(10)

        analyser.stop_record()

    except KeyboardInterrupt:
        analyser.stop_record()
    anylysis = analyser.database.get_all_analyses()
    print(json.dumps(anylysis, indent=4))

    #arp_packet = b"\xff\xff\xff\xff\xff\xff\x08\x00'%\x83~\x08\x06\x00\x01\x08\x00\x06\x04\x00\x01\x08\x00'%\x83~\n\x00\x02\x0f\x00\x00\x00\x00\x00\x00\n\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    #ipv4_packet = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00E\x00\x00Cp\x7f@\x00@\x11\xcb\xf4\x7f\x00\x00\x01\x7f\x00\x005\xb3:\x005\x00/\xfevB7\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x06github\x03com\x00\x00A\x00\x01\x00\x00)\x04\xb0\x00\x00\x00\x00\x00\x00'
    # parsed_data = protocol_parser.parse(ipv4_packet)
    # print(ipv4_packet)
    # print(json.dumps(parsed_data, indent=2, ensure_ascii=False))
    # print("=====================================")
    #
    # parsed_data = protocol_parser.parse(arp_packet)
    # print(arp_packet)
    # print(json.dumps(parsed_data, indent=2, ensure_ascii=False))
    # print("=====================================")
