from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox
from View.components import AnalysisTable


class ViewTerminal(QWidget):
    
    #Constructor for centerApplication viewTerminal
    def __init__(self):
        super().__init__()
        self._initUI()
    

    #initialize the centerApplication viewTerminal
    def _initUI(self):
        
        layout = QVBoxLayout()

        #Create list
        self.table_widget = AnalysisTable()
        layout.addWidget(self.table_widget)

        #Start/Stop-Button
        layoutH = QHBoxLayout()
        self._btnSniff = QPushButton("Start Sniffing")
        self._btnSniff.setToolTip("Start Sniffing Network Data")
        self._btnSniff.setStatusTip("Start Sniffing Network Data")
        layoutH.addWidget(self._btnSniff)

        #ComboBox for Selecting the interface adapter
        self._ComBoxadapter = QComboBox()
        self._ComBoxadapter.setToolTip("Select Network-Adapter for Sniffing")
        self._ComBoxadapter.setStatusTip("Select Network-Adapter for Sniffing")
        layoutH.addWidget(self._ComBoxadapter)

        self.separator = QPushButton("See packets")
        self.separator.setDisabled(True)
        layoutH.addWidget(self.separator)

        self._btnSave = QPushButton("Save")
        self._btnSave.setToolTip("Save Sniffing Network Data")
        self._btnSave.setStatusTip("Save Sniffing Network Data")
        layoutH.addWidget(self._btnSave)

        self._btnLoad = QPushButton("Load")
        self._btnLoad.setToolTip("Load Sniffing Network Data")
        self._btnLoad.setStatusTip("Load Sniffing Network Data")
        layoutH.addWidget(self._btnLoad)


        layout.addLayout(layoutH)
        self.setLayout(layout)


    def addDataSniffing(self, item: tuple[int, str, str]):
        self.table_widget.add_row(item)
