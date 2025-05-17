import threading
from socket import timeout as socket_timeout
from queue import Queue, Empty as QueueEmpty
from typing import Type

from ..ports import DatabasePort
from .services import SocketService, ParserService


class AnalyserCore:
    def __init__(self, database_adapter: Type[DatabasePort]):
        # Ports
        self.database = database_adapter()

        # Services
        self.socket_service = SocketService()
        self.parser_service = ParserService(entry_file="protocols/config/ethernet.json")

        # Logic
        self.stop_event = threading.Event()
        self.packet_queue = Queue(maxsize=1000)
        self.reading_thread = threading.Thread(target=self._read_raw_packets, daemon=True)
        self.storing_thread = threading.Thread(target=self._store_raw_in_db, daemon=True)

        # Variables
        self.alaysis_id = None

    def _read_raw_packets(self):
        while not self.stop_event.is_set():
            try:
                raw_data, addr = self.socket_service.receive()
                if not self.packet_queue.full():
                    self.packet_queue.put(raw_data)
            except socket_timeout:
                continue
            except Exception as e:
                print(f"Error reading packet: {e}")
                break

    def _store_raw_in_db(self):
        while not self.stop_event.is_set() or not self.packet_queue.empty():
            try:
                try:
                    raw_data = self.packet_queue.get(timeout=1.0)
                except QueueEmpty:
                    continue
                src_mac, dst_mac = self.parser_service.get_mac_adress(raw_data)
                self.database.insert_packet(src_mac, dst_mac, raw_data, self.alaysis_id)
                self.packet_queue.task_done()
            except Exception as e:
                print(f"Error processing packet: {e}")
                continue

    def record(self, nic: str) -> None:
        """
        Run the network analyser in detached mode.
        """
        self.database.init_db()
        self.alaysis_id = self.database.insert_analysis(nic)
        if self.alaysis_id is None:
            return
        self.socket_service.set_nic(nic)
        self.stop_event.clear()
        self.reading_thread.start()
        self.storing_thread.start()

    def stop_record(self) -> None:
        """
        Stop the network analyser running in detached mode.
        """
        self.stop_event.set()
        self.packet_queue.join()
        self.reading_thread.join()
        self.storing_thread.join()

        self.database.close_db()
        self.socket_service.close()

        self.alaysis_id = None
