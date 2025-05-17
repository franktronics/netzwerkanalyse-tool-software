import socket
import platform
from typing import Literal, Any

OsType = Literal["Windows", "Linux", "Darwin", "unknown"]

class SocketService:
    def __init__(self, nic: str | None = None) -> None:
        self._os_type: OsType = "unknown"
        self._nic = nic
        self.socket_obj: type[socket.socket] | None = None

    def _socket_linux(self) -> None:
        self.socket_obj = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        self.socket_obj.bind((self._nic, 0))
        self.socket_obj.settimeout(1.0)

    def _socket_windows(self) -> None:
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        host = socket.gethostbyname(socket.gethostname())
        self.socket_obj.bind((host, 0))
        self.socket_obj.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.socket_obj.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON) # enable promiscuous mode

    def _socket_macos(self) -> None:
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        host = socket.gethostbyname(socket.gethostname())
        self.socket_obj.bind((host, 0))

    def _os_detection(self) -> None:
        if self._os_type != "unknown":
            return
        system = platform.system()
        if system not in ["Windows", "Linux", "Darwin"]:
            raise ValueError("Unknown operating system")
        self._os_type = system

    def receive(self) -> tuple[bytes, Any]:
        """
        Receive raw packets from the socket.
        """
        if self._nic is None:
            raise ValueError("Network interface (NIC) is not set")
        self._os_detection()
        if self.socket_obj is not None:
            self.close()
        if self._os_type == "Linux":
            self._socket_linux()
        elif self._os_type == "Windows":
            self._socket_windows()
        elif self._os_type == "Darwin":
            self._socket_macos()
        else:
            raise ValueError("Failed to detect OS type")
        return self.socket_obj.recvfrom(65535)

    def close(self) -> None:
        """
        Close the socket and disable promiscuous mode if applicable.
        """
        if self._os_type == "Windows":
            self.socket_obj.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        self.socket_obj.close()

    def set_nic(self, nic: str) -> None:
        """
        Set the network interface (NIC) for the socket.
        """
        self._nic = nic

    @property
    def get_nic(self) -> str | None:
        return self._nic

