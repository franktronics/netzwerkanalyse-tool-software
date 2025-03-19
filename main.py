from utils.functions import os_detection, nic_detection
from sockets import SocketInit


if __name__ == "__main__":
    os_detected = os_detection()
    nics = nic_detection()

    print(f"Detected OS: {os_detected}")
    print(f"Detected NICs: {nics}")
    #The user must select an interface to sniff on
    selected_nic = ""
    if os_detected == "linux":
        selected_nic = input(f"Please select a NIC (example: {nics[0]}): ")

    SocketInit(os_detected, selected_nic)