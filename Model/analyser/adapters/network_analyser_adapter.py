from ..core import AnalyserCore, ParserCore, Participant, MapBuilderCore
from ..ports import DatabasePort, NetworkAnalyserPort
from .database_adapter import DatabaseAdapter
from .file_manager_adapter import FileManagerAdapter
from typing import Optional, Callable


class NetworkAnalyser(NetworkAnalyserPort):
    def __init__(self):
        self._config = {
            "parser_entry_file": "protocols/config/ethernet.json",
            "parser_types_file": "protocols/config/type.json"
        }

        self._analyser_core = AnalyserCore(DatabaseAdapter)
        self._parser_core = ParserCore(FileManagerAdapter)
        self._database = self._analyser_core.database

    def set_config(self, config: dict) -> None:
        self._config.update(config)
        self._parser_core.set_entry_file(self._config["parser_entry_file"])

    @property
    def database(self) -> DatabasePort:
        return self._database

    def record(self, nic: str, callback: Optional[Callable[[bytes], None]] = None) -> tuple[int, str, str] | None:
        return self._analyser_core.record(nic, callback)

    def stop_record(self) -> None:
        self._analyser_core.stop_record()

    def is_running(self) -> bool:
        return self._analyser_core.running

    def parse_one_packet(self, packet: bytes) -> dict[str, dict[str, any]]:
        return self._parser_core.parse_one_packet(packet)

    def get_participants_map(self, packets: list[tuple[int, str, str, str, str, str]]) -> list[Participant]:
        return MapBuilderCore.build_map(packets)