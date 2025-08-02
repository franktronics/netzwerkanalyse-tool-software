from abc import ABC, abstractmethod
from .database_port import DatabasePort
from typing import Optional, Callable
from ..core import Participant


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
    def record(self, nic: str, callback: Optional[Callable[[bytes], None]] = None) -> tuple[int, str, str] | None:
        """
        Start recording network packets on the specified NIC.

        Args:
            nic (str): The network interface card to monitor.
            callback (Optional[Callable[[], bytes]]): Optional callback function to process packets.

        Returns:
            tuple: A tuple containing the analysis ID, timestamp, and NIC if successful, or None if failed.
        """
        pass

    @abstractmethod
    def stop_record(self) -> None:
        """
        Stop recording network packets.
        """
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """
        Check if the network analyser is currently running.

        Returns:
            bool: True if the analyser is running, False otherwise.
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

    @abstractmethod
    def get_participants_map(self, packets: list[tuple[int, str, str, str, str, str]]) -> list[Participant]:
        """
        Build a map of participants from the recorded packets.

        Args:
            packets (list[tuple[int, str, str, str, str, str]]): List of packets to analyze.

        Returns:
            list[Participant]: List of Participant objects representing the network structure.
        """
        pass