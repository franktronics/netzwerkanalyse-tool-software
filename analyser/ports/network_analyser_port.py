from abc import ABC, abstractmethod
from analyser.ports import DatabasePort


class NetworkAnalyserPort(ABC):

    @abstractmethod
    def set_config(self, config: dict) -> None:
        """
        Set the configuration for the network analyser.

        Args:
            config (dict): Configuration dictionary containing settings for the analyser.
        """
        pass

    @property
    @abstractmethod
    def database(self) -> DatabasePort:
        """
        Returns the database adapter.

        Returns:
            DatabasePort: The database adapter instance.
        """
        pass

    @abstractmethod
    def record(self, nic: str) -> None:
        """
        Start recording network packets on the specified NIC.

        Args:
            nic (str): The network interface card to monitor.
        """
        pass

    @abstractmethod
    def stop_record(self) -> None:
        """
        Stop recording network packets.
        """
        pass

    @abstractmethod
    def parse_one_packet(self, packet: bytes) -> dict[str, dict[str, any]]:
        """
        Parse a single network packet.

        Args:
            packet (bytes): The raw packet data to parse.

        Returns:
            dict: Parsed packet data structured as a dictionary.
        """