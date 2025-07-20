from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, QModelIndex
import os

class ControllerAnalyzedData:

    def __init__(self, view, model):
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
        self._view._viewanalyzedData.btn_statistics.released.connect(self._actionPerformedStatistics)
        self._view._viewanalyzedData.table_database.getTable().doubleClicked.connect(self._actionPerformedDatabaseDoubleClick)
        self._view._viewanalyzedData.table_database.getTable().clicked.connect(self._actionPerformedDatabaseSingleClick)
        self._view._viewanalyzedData.table_packages.getTable().doubleClicked.connect(self._actionPerformedPackagesDoubleClick)
        self._view._viewanalyzedData.table_packages.getTable().clicked.connect(self._actionPerformedPackagesSingleClick)
        self._view._viewanalyzedData.btnRefreshTable.released.connect(self._actionPerformedReloadTable)

    

    def _actionPerformedReloadTable(self):
        print("self._model.get_all_analyses()")
        self._model.get_all_analyses()



    def _actionPerformedBack(self):
        self._model.viewAnalyzedBack()



    def _actionPerformedNext(self):
        if self._model.retViewAnalyzedState() == self._model._settings_view.STATEDATABASE:
            if self.rowSelected_database is not None:
                self._model.viewAnalyzedNext()
                print("self._model.get_packets_by_analysis_id(analysis_id)")
                print(str("database: ") + str(self.rowSelected_database))

                analysis_id = int(self._view._viewanalyzedData.table_database.item(self.rowSelected_database, 0))
                self._model.get_packets_by_analysis_id(analysis_id)
                self.rowSelected_database = None
            
            else:
                self._error()

        elif self._model.retViewAnalyzedState() == self._model._settings_view.STATEPACKAGE:
            if self.rowSelected_packages is not None:
                self._model.viewAnalyzedNext()
                print("self._model.parse_one_packet(analysis_id)")
                print(str("pack: ") + str(self.rowSelected_packages))

                packet_id: int = int(self._view._viewanalyzedData.table_packages.item(self.rowSelected_packages, 0))
                self._model.get_packet_dict(packet_id)
                self.rowSelected_packages = None
            else:
                self._error()


    def _actionPerformedStatistics(self):
        if self._model.retViewAnalyzedState() == self._model._settings_view.STATEDATABASE:
            if self.rowSelected_database is not None:
                self._model.viewAnalyzedStatistics()
                print("self._model.get_packets_by_analysis_id(analysis_id)")
                print(str("database: ") + str(self.rowSelected_database))

                analysis_id = int(self._view._viewanalyzedData.table_database.item(self.rowSelected_database, 0))
                self._model.get_packets_by_analysis_id(analysis_id)
                self.rowSelected_database = None
            
            else:
                self._error()
            
    def _error(self):
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

    
    