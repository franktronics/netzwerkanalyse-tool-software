from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .components import NetworkCanvas

class ViewStatistics(QWidget):
    
    #Constructor for centerApplication viewLStatistics
    def __init__(self):
        super().__init__()
        self._initUI()
    

    #initialize the centerApplication viewStatistics
    def _initUI(self):
        layout = QVBoxLayout()

        # Network canvas for visualization
        self.network_canvas = NetworkCanvas()
        self.network_canvas.add_participant(id = "00:11:22:33:44:55", name = "PC1")
        self.network_canvas.add_participant(id = "66:77:88:99:AA:BB", name = "PC2")
        self.network_canvas.add_participant(id = "77:77:88:99:AA:BC", name = "PC3")
        self.network_canvas.add_participant(id = "88:99:AA:BB:CC:DD", name = "PC4")
        self.network_canvas.add_participant(id = "99:AA:BB:CC:DD:EE", name = "PC5")
        self.network_canvas.add_participant(id = "AA:BB:CC:DD:EE:FF", name = "Router")

        self.network_canvas.add_connection(if_from = "00:11:22:33:44:55", id_to = "AA:BB:CC:DD:EE:FF")
        self.network_canvas.add_connection(if_from = "00:11:22:33:44:55", id_to = "66:77:88:99:AA:BB")

        self.network_canvas.add_connection(if_from="66:77:88:99:AA:BB", id_to="AA:BB:CC:DD:EE:FF")

        self.network_canvas.add_connection(if_from="77:77:88:99:AA:BC", id_to="AA:BB:CC:DD:EE:FF")
        self.network_canvas.add_connection(if_from="77:77:88:99:AA:BC", id_to="88:99:AA:BB:CC:DD")

        self.network_canvas.add_connection(if_from="88:99:AA:BB:CC:DD", id_to="AA:BB:CC:DD:EE:FF")
        self.network_canvas.add_connection(if_from="88:99:AA:BB:CC:DD", id_to="77:77:88:99:AA:BC")

        self.network_canvas.add_connection(if_from="99:AA:BB:CC:DD:EE", id_to="66:77:88:99:AA:BB")

        layout.addWidget(self.network_canvas)

        self.setLayout(layout)


    def addData(self, data):
        #todo
        #self.clear()
        pass

    #Todo: clear-Methode in networkCanvas
    #addData(): füllen: Auswahl der einzelnen Informationen