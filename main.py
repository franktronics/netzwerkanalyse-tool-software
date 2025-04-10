from utils.functions import os_detection, nic_detection
from sockets import SocketInit, SocketReader
from protocols.parser import EthernetParser


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
    ethernet_parser = EthernetParser()
    socket_reader = SocketReader(socket_obj=socket_obj, reader=ethernet_parser.run)

    socket_reader.run()
