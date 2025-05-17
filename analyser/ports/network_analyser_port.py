from abc import ABC, abstractmethod
from analyser.ports import DatabasePort


class NetworkAnalyserPort(ABC):

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