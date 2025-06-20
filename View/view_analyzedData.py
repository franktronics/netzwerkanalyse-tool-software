from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTableView, QListWidget, QToolBar, QMainWindow, QComboBox, QLabel
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QHeaderView
import os
from View.components.tableTemplateV1 import TableTemplateV1

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


        self._initUI()
    

    #initialize the centerApplication ViewRawData
    def _initUI(self):

        self.layoutH_lab = QHBoxLayout()

        #Labels
        self.lab_databaseSelection = QLabel("Select the database")
        self.lab_databaseSelection.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutH_lab.addWidget(self.lab_databaseSelection)

        self.lab_packageSelection = QLabel("Select the package")
        self.lab_packageSelection.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutH_lab.addWidget(self.lab_packageSelection)

        #Tables/Lists
        self.table_database = TableTemplateV1(["ID", "Timestamp", "NIC"])
        #self.table_database.addTestData(5)

        self.table_packages = TableTemplateV1(["ID", "Timestamp", "Src-MAC", "Dst-MAC", "RAW-Data"])
        #self.table_packages.addTestData(2)

        self.list_package = QListWidget()
        #self.list_package.addItems(["sfsfsfsf", "dfshgksghmj", "dafoihgnadonhgfaä#nm", "3ß49857"])
        
        
        #Buttons
        self.layoutH_btn = QHBoxLayout()
        self.btn_back = QPushButton("Back")
        self.layoutH_btn.addWidget(self.btn_back)

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
        self.lab_packageSelection.setStyleSheet("""
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
        self.lab_packageSelection.setStyleSheet("""
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
        self.lab_packageSelection.setStyleSheet("""
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

        self._replace_dataWidget(self.list_package)

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
        self.lab_packageSelection.setStyleSheet("""
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


    def _replace_dataWidget(self, new_widget):
        layout = self.layout()

        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, (QTableView, QListWidget)):
                # Alte Tabelle entfernen
                layout.removeWidget(widget)
                widget.setParent(None)

                # Neue Tabelle einfügen am selben Index
                layout.insertWidget(i, new_widget)
                break

    
    def reloadAnalysis(self, data):
        self.table_database.addRow(data)

    def reloadPackages(self, data):
        self.table_packages.addRow(data)