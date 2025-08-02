from PyQt6.QtWidgets import QWidget, QVBoxLayout
from dataclasses import dataclass
from .components import NetworkCanvas


@dataclass
class Participant:
    mac: str
    name: str
    recipients: list[str]


class ViewStatistics(QWidget):

    # Constructor for centerApplication viewLStatistics
    def __init__(self):
        super().__init__()
        self.network_canvas: NetworkCanvas = NetworkCanvas()
        self._initUI()

    # initialize the centerApplication viewStatistics
    def _initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.network_canvas)
        self.setLayout(layout)

    def addData(self, data: list[Participant]):
        self.network_canvas.clear_canvas()
        for participant in data:
            # Add participant to the network canvas
            self.network_canvas.add_participant(id=participant.mac, name=participant.name)
        for participant in data:
            for recipient in participant.recipients:
                # Add connection to the network canvas
                self.network_canvas.add_connection(id_from=participant.mac, id_to=recipient)