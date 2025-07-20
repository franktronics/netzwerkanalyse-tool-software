from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTableView, QTreeView, QComboBox, QLabel
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QHeaderView
import os
from View.components.tableTemplateV1 import TableTemplateV1
from View.components.treeTemplateV1 import TreeTemplateV1
from View.view_statistics import ViewStatistics

class ViewAnalyzedData(QWidget):
    #Constructor for centerApplication ViewRawData
    def __init__(self):
        super().__init__()

        self.selectedDatabase = None
        self.selectedPackage = None

        self.STATEDEFAULT = 0
        self.STATEDATABASE = 1
        self.STATEPACKAGE = 2
        self.STATESHOW = 3
        self.STATESTATISTICS = 4


        self._initUI()
    

    #initialize the centerApplication ViewRawData
    def _initUI(self):

        base_path = os.path.dirname(__file__)
        icon_path = os.path.join(base_path, "images")

        self.layoutH_lab = QHBoxLayout()

        #Labels
        self.lab_databaseSelection = QLabel("Select the database")
        self.lab_databaseSelection.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutH_lab.addWidget(self.lab_databaseSelection)

        self.lab_packageAnalysis = QLabel("package analysis")
        self.lab_packageAnalysis.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutH_lab.addWidget(self.lab_packageAnalysis)

        #icon refresh nics
        self.btnRefreshTable = QPushButton()
        icon_path_temp = os.path.join(icon_path, "refresh-icon.png")
        icon = QIcon(icon_path_temp)

        self.btnRefreshTable.setIcon(icon)
        self.btnRefreshTable.setIconSize(QSize(20, 20))
        self.btnRefreshTable.setFixedSize(23, 23)
        self.btnRefreshTable.setFlat(True)
        self.layoutH_lab.addWidget(self.btnRefreshTable)

        #Tables/Lists
        self.table_database = TableTemplateV1(["ID", "Timestamp", "NIC"])
        #self.table_database.addTestData(5)

        self.table_packages = TableTemplateV1(["ID", "Timestamp", "Src-MAC", "Dst-MAC", "RAW-Data", "Analysis-ID"])
        #self.table_packages.addTestData(2)

        self.tree_package = TreeTemplateV1()
        #self.tree_package.showTestData()

        self.graphic_statistics = ViewStatistics()
        
        
        #Buttons
        self.layoutH_btn = QHBoxLayout()
        self.btn_back = QPushButton("Back")
        self.layoutH_btn.addWidget(self.btn_back)

        self.btn_nvm = QPushButton()
        self.btn_nvm.setDisabled(True)
        self.layoutH_btn.addWidget(self.btn_nvm)

        self.btn_statistics = QPushButton("Graphical Analysis")
        self.layoutH_btn.addWidget(self.btn_statistics)

        self.btn_next = QPushButton("Next")
        self.layoutH_btn.addWidget(self.btn_next)

        layout = QVBoxLayout()
        layout.addLayout(self.layoutH_lab)
        layout.addWidget(QTableView())
        layout.addLayout(self.layoutH_btn)

        self.setLayout(layout)
    

    def setState(self, state):
        if state == self.STATEDEFAULT:
            self._state_default()
        elif state == self.STATEDATABASE:
            self._state_database()
        elif state == self.STATEPACKAGE:
            self._state_package()
        elif state == self.STATESHOW:
            self._state_show()
        elif state == self.STATESTATISTICS:
            self._state_statistics()

    
    def _state_database(self):
        #Labels
        self.lab_databaseSelection.setStyleSheet("""
                QLabel {
                    background-color: grey;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        self.lab_packageAnalysis.setStyleSheet("""
                QLabel {
                    background-color: none;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        
        #Buttons
        self.btn_back.setDisabled(True)
        self.btn_next.setDisabled(False)
        self.btn_statistics.setDisabled(False)
        self.btn_nvm.setDisabled(True)

        self._replace_dataWidget(self.table_database.getTable())
        
    def _state_package(self):
        #Labels
        self.lab_databaseSelection.setStyleSheet("""
                QLabel {
                    background-color: green;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        self.lab_packageAnalysis.setStyleSheet("""
                QLabel {
                    background-color: grey;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        
        #Buttons
        self.btn_back.setDisabled(False)
        self.btn_next.setDisabled(False)
        self.btn_statistics.setDisabled(True)
        self.btn_nvm.setDisabled(True)

        self._replace_dataWidget(self.table_packages.getTable())

    def _state_show(self):
        #Labels
        self.lab_databaseSelection.setStyleSheet("""
                QLabel {
                    background-color: green;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        self.lab_packageAnalysis.setStyleSheet("""
                QLabel {
                    background-color: green;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        
        #Buttons
        self.btn_back.setDisabled(False)
        self.btn_next.setDisabled(True)
        self.btn_statistics.setDisabled(True)
        self.btn_nvm.setDisabled(True)

        self._replace_dataWidget(self.tree_package.getTree())


    def _state_statistics(self):
        #Labels
        self.lab_databaseSelection.setStyleSheet("""
                QLabel {
                    background-color: green;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        self.lab_packageAnalysis.setStyleSheet("""
                QLabel {
                    background-color: green;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        
        #Buttons
        self.btn_back.setDisabled(False)
        self.btn_next.setDisabled(True)
        self.btn_statistics.setDisabled(True)
        self.btn_nvm.setDisabled(True)

        self._replace_dataWidget(self.graphic_statistics)

    def _state_default(self):
        #Labels
        self.lab_databaseSelection.setStyleSheet("""
                QLabel {
                    background-color: none;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        self.lab_packageAnalysis.setStyleSheet("""
                QLabel {
                    background-color: none;
                    color: black;
                    border: 1px solid black;
                    padding: 4px;
                }
            """)
        
        #Buttons
        self.btn_back.setDisabled(False)
        self.btn_next.setDisabled(False)
        self.btn_statistics.setDisabled(False)
        self.btn_nvm.setDisabled(True)


    def _replace_dataWidget(self, new_widget):
        layout = self.layout()

        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, (QTableView, QTreeView, ViewStatistics)):
                # Alte Tabelle entfernen
                layout.removeWidget(widget)
                widget.setParent(None)

                # Neue Tabelle einfügen am selben Index
                layout.insertWidget(i, new_widget)
                break

    
    def loadAnalysis(self, data):
        self.table_database.addData(data)

    def loadPackages(self, data):
        self.table_packages.addData(data)
        self.graphic_statistics.addData(data)

    def showAnalysis(self, data: dict[str, dict[str, any]]):
        self.tree_package.showData(data)