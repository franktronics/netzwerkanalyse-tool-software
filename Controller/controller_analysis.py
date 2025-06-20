from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, QModelIndex
import os
from Model import Model

class ControllerAnalysis():

    def __init__(self, view, model:Model):
        self._view = view
        self._model = model

        base_path = os.path.dirname(__file__)
        icon_path = os.path.join(base_path, "icons")
        icon_path_temp = os.path.join(icon_path, "error.png")
        self.icon_error = QIcon(icon_path_temp)

        self.rowSelected_database = None
        self.rowSelected_packages = None


    #Register Events for view-components
    def registerEvents(self):
        #self._view.getMenuActionNew().triggered.connect(self._actionPerformedNew)
        # self._view.getMenuActionOpen().triggered.connect(self._actionPerformedOpen)
        self._view._viewanalyzedData.btn_back.released.connect(self._actionPerformedBack)
        self._view._viewanalyzedData.btn_next.released.connect(self._actionPerformedNext)
        self._view._viewanalyzedData.table_database.getTable().doubleClicked.connect(self._actionPerformedDatabaseDoubleClick)
        self._view._viewanalyzedData.table_database.getTable().clicked.connect(self._actionPerformedDatabaseSingleClick)
        self._view._viewanalyzedData.table_packages.getTable().doubleClicked.connect(self._actionPerformedPackagesDoubleClick)
        self._view._viewanalyzedData.table_packages.getTable().clicked.connect(self._actionPerformedPackagesSingleClick)

    

    def _actionPerformedReloadDatabase(self):
        print("self._model.get_all_analyses()")



    def _actionPerformedBack(self):
        self._model.viewAnalyzedBack()



    def _actionPerformedNext(self):
        if self.rowSelected_database != None:
            self._model.viewAnalyzedNext()
            print("self._model.get_packets_by_analysis_id(self.rowSelected_database)")
            print(str("database: ") + str(self.rowSelected_database))

            self._model.get_packets_by_analysis_id(self.rowSelected_database)
            self.rowSelected_database = None

        elif self.rowSelected_packages != None:
            self._model.viewAnalyzedNext()
            print("self._model.get_analysis_by_id(self.rowSelected_packages)")
            print(str("pack: ") + str(self.rowSelected_packages))

            self._model.get_analysis_by_id(self.rowSelected_packages)
            self.rowSelected_packages = None

        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setWindowIcon(self.icon_error)
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.setText("No entry selected")
            msgBox.exec()


    def _actionPerformedDatabaseSingleClick(self, index: QModelIndex):
        self.rowSelected_database = index.row()


    def _actionPerformedDatabaseDoubleClick(self, index: QModelIndex):
        self.rowSelected_database = index.row()
        self._actionPerformedNext()


    def _actionPerformedPackagesSingleClick(self, index: QModelIndex):
        self.rowSelected_packages = index.row()


    def _actionPerformedPackagesDoubleClick(self, index: QModelIndex):
        self.rowSelected_packages = index.row()
        self._actionPerformedNext()

    
    