from utils.functions import os_detection, nic_detection
from sockets import SocketInit, SocketReader
from protocols.parser import ProtocolParser


if __name__ == "__main__":
    os_detected = os_detection()
    nics = nic_detection()

    print(f"Detected OS: {os_detected}")
    print(f"Detected NICs: {nics}")
    #The user must select an interface to sniff on
    selected_nic = ""
    if os_detected == "linux":
        selected_nic = input(f"Please select a NIC (example: {nics[0]}): ")

    socket_obj = SocketInit(os_detected, selected_nic)
    parser = ProtocolParser(entry_file="protocols/config/ethernet.json")
    socket_reader = SocketReader(socket_obj=socket_obj, parser_fct=parser.parse)

    socket_reader.run()
