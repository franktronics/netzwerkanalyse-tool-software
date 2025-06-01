from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QTabWidget, QToolBar, QMainWindow


class ViewStatistics(QWidget):
    
    #Constructor for centerApplication viewLStatistics
    def __init__(self):
        super().__init__()
        self._initUI()
    

    #initialize the centerApplication viewStatistics
    def _initUI(self):

        layout = QVBoxLayout()

        # Liste zur Anzeige der Pakete
        self.list_widget = QLabel("I only believe the statistics that I have falsified myself")
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        