from ..core import AnalyserCore
from ..adapters import DatabaseAdapter
from ..ports import DatabasePort, NetworkAnalyserPort


class NetworkAnalyser(NetworkAnalyserPort):
    def __init__(self):
        self._core = AnalyserCore(DatabaseAdapter)
        self._database = self._core.database

    @property
    def database(self) -> DatabasePort:
        return self._database

    def record(self, nic: str) -> None:
        self._core.record(nic)

    def stop_record(self) -> None:
        self._core.stop_record()