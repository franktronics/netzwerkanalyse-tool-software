from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTableView, QTabWidget, QToolBar, QMainWindow, QComboBox, QFrame
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
        self.icon_path = os.path.join(base_path, "images")

        layout = QVBoxLayout()

        # self.itemmodel = QStandardItemModel()
        # self.itemmodel.setHorizontalHeaderLabels(["ID", "Timestamp", "Info"])

        # self.table = QTableView()
        # self.table.setModel(self.itemmodel)
        # self.table.horizontalHeader().setStretchLastSection(True)
        # self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        # self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        self.container = QFrame()
        self.container.setObjectName("borderFrame")
        self.container.setFrameShape(QFrame.Shape.NoFrame)
        self.container.setLineWidth(2)
        self.container.setStyleSheet("#borderFrame { border: 2px solid transparent; border-radius: 5px; margin: 2pt;}")

        conlayout = QVBoxLayout(self.container)
        
        #Create table
        self.table = RawDataTable()
        conlayout.addWidget(self.table)
        layout.addWidget(self.container)

        #Start/Stop-Button
        #icon start sniffing
        layoutH = QHBoxLayout()
        self._btnStartSniffing = QPushButton()
        icon_path_temp = os.path.join(self.icon_path, "start-icon.png")
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
        icon_path_temp = os.path.join(self.icon_path, "stop-icon.png")
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
        icon_path_temp = os.path.join(self.icon_path, "refresh-icon.png")
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

        self.activateSniffing()
        # self.setStyleSheet('border-style: solid')
        # self.setStyleSheet('border-color: green')


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

    def activateSniffing(self):
        icon_path_temp = os.path.join(self.icon_path, "start-icon.png")
        icon = QIcon(icon_path_temp)
        self._btnStartSniffing.setIcon(icon)
        self._btnStartSniffing.setEnabled(True)

        icon_path_temp = os.path.join(self.icon_path, "stop-icon_notactivated.png")
        icon = QIcon(icon_path_temp)
        self._btnStopSniffing.setIcon(icon)
        self._btnStopSniffing.setEnabled(False)

        self.container.setStyleSheet("#borderFrame { border: 2px solid transparent; border-radius: 5px; margin: 2pt;}")

    def deactivateSniffing(self):
        icon_path_temp = os.path.join(self.icon_path, "start-icon_notactivated.png")
        icon = QIcon(icon_path_temp)
        self._btnStartSniffing.setIcon(icon)
        self._btnStartSniffing.setEnabled(False)

        icon_path_temp = os.path.join(self.icon_path, "stop-icon.png")
        icon = QIcon(icon_path_temp)
        self._btnStopSniffing.setIcon(icon)
        self._btnStopSniffing.setEnabled(True)

        self.container.setStyleSheet("#borderFrame { border: 2px solid #55DD33; border-radius: 5px; margin: 2pt;}")