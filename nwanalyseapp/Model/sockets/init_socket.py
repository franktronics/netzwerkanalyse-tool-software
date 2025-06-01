#from utils.functions import OsType
import socket

class SocketInit:
    def __init__(self):
        self.os_type = None
        self.nic = None
        self.socket_obj: type[socket.socket] = None


    def configureSocket(self, os_type, nic: str):
        if self.socket_obj != None:
            self.socket_obj.close()
        
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


    # def __init__(self, os_type: OsType, nic: str):
    #     self.os_type = os_type
    #     self.nic = nic
    #     self.socket_obj: type[socket.socket] = None

    #     if os_type == "unknown":
    #         raise ValueError("Unknown operating system")
    #     if os_type == "windows":
    #         self.windows()
    #     elif os_type == "linux":
    #         self.linux()
    #     elif os_type == "macos":
    #         self.macos()

    def linux(self):
        self.socket_obj = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        self.socket_obj.bind((self.nic, 0))
        self.socket_obj.setblocking(0)

    def windows(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        host = socket.gethostbyname(socket.gethostname())
        self.socket_obj.bind((host, 0))
        self.socket_obj.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.socket_obj.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON) # enable promiscuous mode
        self.socket_obj.setblocking(0)

    def macos(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        host = socket.gethostbyname(socket.gethostname())
        self.socket_obj.bind((host, 0))
        self.socket_obj.setblocking(0)

    def receive(self):
        try:
            retData = self.socket_obj.recvfrom(65535)
        except Exception as error:
            print(str(error))
            retData = (-1)
        return retData

    def close(self):
        if self.os_type == "windows":
            self.socket_obj.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        self.socket_obj.close()

    def fileno(self):
        return self.socket_obj.fileno()