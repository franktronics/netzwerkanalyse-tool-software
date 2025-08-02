from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, fields


@dataclass
class AnalyserModel:
    protocol_entry_file: str
    network_interface: str

    def merge(self, other: AnalyserModel) -> None:
        if not isinstance(other, AnalyserModel):
            raise TypeError("Can only merge with another AnalyserModel instance")
        for field in fields(self):
            other_value = getattr(other, field.name)
            if other_value is not None:
                setattr(self, field.name, deepcopy(other_value))