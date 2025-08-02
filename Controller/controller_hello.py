from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, QModelIndex
import os

class ControllerHello():

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
        self._view._viewHello.btn_start.released.connect(self._actionPerformedStart)

    

    def _actionPerformedStart(self):
        self._view.setWindow(self._view.VIEWRAWDATA)