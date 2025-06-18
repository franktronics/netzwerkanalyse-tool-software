from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QTabWidget, QToolBar, QMainWindow


class ViewTable(QWidget):
    
    #Constructor for centerApplication viewTable
    def __init__(self):
        super().__init__()
        self._initUI()
    

    #initialize the centerApplication viewList
    def _initUI(self):
        
        layout = QVBoxLayout()

        #Start/Stop-Button
        self._btnLoadData = QPushButton("Load Data")
        self._btnLoadData.setToolTip("Load Data")
        self._btnLoadData.setStatusTip("Load Data")
        layout.addWidget(self._btnLoadData)

        self.setLayout(layout)