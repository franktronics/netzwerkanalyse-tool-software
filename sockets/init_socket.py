from utils.functions import OsType
import socket

class SocketInit:
    def __init__(self, os_type: OsType, nic: str):
        self.os_type = os_type
        self.nic = nic
        self.socket_obj: type[socket.socket] = None

        if os_type == "unknown":
            raise ValueError("Unknown operating system")
        if os_type == "windows":
            self.windows()
        elif os_type == "linux":
            self.linux()
        elif os_type == "macos":
            self.macos()

    def linux(self):
        self.socket_obj = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
        self.socket_obj.bind((self.nic, 0))

        #only for testing
        while True:
            packet = self.socket_obj.recv(65535)
            print(packet)
            print("===")

    def windows(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        host = socket.gethostbyname(socket.gethostname())
        self.socket_obj.bind((host, 0))
        self.socket_obj.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.socket_obj.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON) # enable promiscuous mode

        # only for testing
        while True:
            packet = self.socket_obj.recv(65535)
            print(packet)
            print("===")

    def macos(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        host = socket.gethostbyname(socket.gethostname())
        self.socket_obj.bind((host, 0))

        # only for testing
        while True:
            packet = self.socket_obj.recv(65535)
            print(packet)
            print("===")

    def close(self):
        if self.os_type == "windows":
            self.socket_obj.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        self.socket_obj.close()