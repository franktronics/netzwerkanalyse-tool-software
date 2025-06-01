from PyQt6.QtWidgets import QApplication
from View.view import View
from Controller.menucontroller import MenuController
from Model.model import Model
from Controller.rawdata_controller import RawDataController
from Adapter.terminalstatusadapter import TerminalStatusAdapter
from Adapter.windowconfigadapter import WindowConfigAdapter
from Adapter.terminalnicadapter import TerminalNicAdapter
from Adapter.terminaldataadapter import TerminalDataAdapter
from util.subpub.subpubv2 import SubPubV2
import time

if __name__ == "__main__":
    app = QApplication([])

    subpub = SubPubV2()

    #View
    view = View()
    
    #Model
    model = Model(subpub)
    model.subscribeSniffer()

    #Controller
    rawDataController = RawDataController(view, model)
    menucontroller = MenuController(view, model)
    
    #Adapter
    terminalStatusAdapter = TerminalStatusAdapter(view, model, subpub)
    terminalnicAdapter = TerminalNicAdapter(view, model, subpub)
    windowconfigAdapter = WindowConfigAdapter(view, model, subpub)
    terminalDataAdapter = TerminalDataAdapter(view, model, subpub)

    model.snifferDetectOS()
    model.snifferDetectNic()


    view.initializeWindow()
    rawDataController.registerEvents()
    menucontroller.registerEvents()
    terminalStatusAdapter.subscribeModel_StatusSniffingData()
    terminalnicAdapter.subscribeModel_NicDataComboBox()
    windowconfigAdapter.subscribeModel_WindowConfiguration()
    terminalDataAdapter.subscribeModel_TerminalDataSniffing()

    app.exec()