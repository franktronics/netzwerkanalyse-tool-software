from abc import ABC, abstractmethod
from typing import Tuple

class DatabasePort(ABC):
    """
    Abstract base class for database operations.
    """

    @abstractmethod
    def insert_analysis(self, nic: str) -> tuple[int, str, str] | None:
        """
        Insert a new analysis record.

        Args:
            nic (str): Network Interface Card identifier

        Returns:
            tuple: Analysis record as (id, timestamp, nic) or None if failed
        """
        pass

    @abstractmethod
    def insert_packet(self, src_mac: str, dst_mac: str, raw_data: bytes, analysis_id: int) -> int | None:
        """
        Insert a new packet record.

        Args:
            dst_mac (str): Destination MAC address
            src_mac (str): Source MAC address
            raw_data (bytes): Raw packet data
            analysis_id (int, optional): ID of the associated analysis

        Returns:
            int: ID of the newly inserted packet record or None if failed
        """
        pass

    @abstractmethod
    def get_analysis_by_id(self, analysis_id: int) -> Tuple[int, str, str] | None:
        """
        Get analysis record by ID.

        Args:
            analysis_id (int): ID of the analysis to retrieve

        Returns:
            tuple: Analysis record as (id, timestamp, nic) or None if not found
        """
        pass

    @abstractmethod
    def get_packets_by_analysis_id(self, analysis_id: int) -> list[Tuple[int, str, str, str, str, str]] | None:
        """
        Get all packets associated with a specific analysis ID.

        Args:
            analysis_id (int): ID of the analysis

        Returns:
            list: List of packet records as (id, timestamp, src_mac, dst_mac, raw_data, analysis_id)
        """
        pass

    @abstractmethod
    def get_all_analyses(self) -> list[Tuple[int, str, str]] | None:
        """
        Get all analysis records.

        Returns:
            list: List of analysis records as (id, timestamp, nic)
        """
        pass

    @abstractmethod
    def delete_analysis(self, analysis_id: int) -> bool:
        """
        Delete an analysis and all its associated packets.

        Args:
            analysis_id (int): ID of the analysis to delete

        Returns:
            bool: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def close_db(self) -> None:
        """
        Safely close the database connection.

        Returns:
            None
        """
        pass

    @abstractmethod
    def init_db(self) -> None:
        """
        Initialize the database and create necessary tables.

        Returns:
            None
        """
        pass