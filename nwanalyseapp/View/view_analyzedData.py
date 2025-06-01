from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QTabWidget, QToolBar, QMainWindow, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
import os

class ViewAnalyzedData(QWidget):
    
    #Constructor for centerApplication ViewRawData
    def __init__(self):
        super().__init__()
        self._initUI()
    

    #initialize the centerApplication ViewRawData
    def _initUI(self):
        
        base_path = os.path.dirname(__file__)
        icon_path = os.path.join(base_path, "images")

        layout = QVBoxLayout()

        #Create list
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        #Start/Stop-Button
        layoutH = QHBoxLayout()
        self._btnStartSniffing = QPushButton()
        icon_path_temp = os.path.join(icon_path, "start-icon.png")
        icon = QIcon(icon_path_temp)

        self._btnStartSniffing.setToolTip("Start Sniffing Network Data")
        self._btnStartSniffing.setStatusTip("Start Sniffing Network Data")
        self._btnStartSniffing.setIcon(icon)
        self._btnStartSniffing.setIconSize(QSize(20, 20))
        self._btnStartSniffing.setFixedSize(23, 23)
        self._btnStartSniffing.setFlat(True)
        layoutH.addWidget(self._btnStartSniffing)

        self._btnStopSniffing = QPushButton()
        icon_path_temp = os.path.join(icon_path, "stop-icon.png")
        icon = QIcon(icon_path_temp)

        self._btnStopSniffing.setToolTip("Stop Sniffing Network Data")
        self._btnStopSniffing.setStatusTip("Stop Sniffing Network Data")
        self._btnStopSniffing.setIcon(icon)
        self._btnStopSniffing.setIconSize(QSize(20, 20))
        self._btnStopSniffing.setFixedSize(23, 23)
        self._btnStopSniffing.setFlat(True)
        layoutH.addWidget(self._btnStopSniffing)

        #ComboBox for Selecting the interface adapter
        self._ComBoxadapter = QComboBox()
        self._ComBoxadapter.setToolTip("Select Network-Adapter for Sniffing")
        self._ComBoxadapter.setStatusTip("Select Network-Adapter for Sniffing")
        layoutH.addWidget(self._ComBoxadapter)


        self._btnRefreshNic = QPushButton()
        icon_path_temp = os.path.join(icon_path, "refresh-icon.png")
        icon = QIcon(icon_path_temp)

        self._btnRefreshNic.setIcon(icon)
        self._btnRefreshNic.setIconSize(QSize(20, 20))
        self._btnRefreshNic.setFixedSize(23, 23)
        self._btnRefreshNic.setFlat(True)
        layoutH.addWidget(self._btnRefreshNic)


        self.separator = QPushButton()
        self.separator.setDisabled(True)
        layoutH.addWidget(self.separator)

        self._btnExport = QPushButton("Export data")
        self._btnExport.setToolTip("Export Sniffing Network Data")
        self._btnExport.setStatusTip("Export Sniffing Network Data")
        layoutH.addWidget(self._btnExport)

        # self._btnLoad = QPushButton("Load")
        # self._btnLoad.setToolTip("Load Sniffing Network Data")
        # self._btnLoad.setStatusTip("Load Sniffing Network Data")
        # layoutH.addWidget(self._btnLoad)


        layout.addLayout(layoutH)
        self.setLayout(layout)


    # Add raw-data to window
    def addDataSniffing(self, item):
        self.list_widget.addItem(item)

    # Update Combobox-Adapter
    def updateNics(self, nics):
        self._ComBoxadapter.clear()
        self._ComBoxadapter.addItems(nics)