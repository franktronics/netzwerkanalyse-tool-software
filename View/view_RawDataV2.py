from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTableView, QTabWidget, QToolBar, QMainWindow, QComboBox
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QHeaderView
from View.components.rawData_table import RawDataTable
import os

class ViewRawDataV2(QWidget):
    
    #Constructor for centerApplication ViewRawData
    def __init__(self):
        super().__init__()
        self._initUI()
    

    #initialize the centerApplication ViewRawData
    def _initUI(self):
        
        base_path = os.path.dirname(__file__)
        icon_path = os.path.join(base_path, "images")

        layout = QVBoxLayout()

        # self.itemmodel = QStandardItemModel()
        # self.itemmodel.setHorizontalHeaderLabels(["ID", "Timestamp", "Info"])

        # self.table = QTableView()
        # self.table.setModel(self.itemmodel)
        # self.table.horizontalHeader().setStretchLastSection(True)
        # self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        # self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        #Create table
        self.table = RawDataTable()
        layout.addWidget(self.table)

        #Start/Stop-Button
        #icon start sniffing
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

        #icon stop sniffing
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

        #icon refresh nics
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


    # Add sniffingdata to table
    # def addSniffingData(self, item):
    #     items = [QStandardItem(str(data)) for data in item]
    #     self.itemmodel.appendRow(items)

    #new function for adding data to the rawdata_table
    def addSniffingData(self, item: tuple[int, str, str]):
        self.table.add_row(item)

    # Update Combobox-Adapter
    def updateNics(self, nics):
        self._ComBoxadapter.clear()
        self._ComBoxadapter.addItems(nics)