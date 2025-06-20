from PyQt6.QtWidgets import QApplication
# from View.view import View
from View.view_V2 import ViewV2
from Model.model import Model

# Controller
from Controller.terminalcontroller import TerminalController
from Controller.menucontroller import MenuController
from Controller.rawdata_controller import RawDataController
from Controller.controller_analysis import ControllerAnalysis
from Controller.controller_hello import ControllerHello

from Adapter.terminalstatusadapter import TerminalStatusAdapter
from Adapter.windowconfigadapter import WindowConfigAdapter
from Adapter.terminalnicadapter import TerminalNicAdapter
from Adapter.terminaldataadapter import TerminalDataAdapter
from Adapter.adapter_analyzedData import AdapterAnalyzedData
from util.subpub.subpubv2 import SubPubV2

if __name__ == "__main__":
    app = QApplication([])

    subpub = SubPubV2()

    #View
    view = ViewV2()
    
    #Model
    model = Model(subpub)

    #Controller
    # terminalController = TerminalController(view, model)
    rawDataController = RawDataController(view, model)
    menucontroller = MenuController(view, model)
    controllerAnalyzedData = ControllerAnalysis(view, model)
    controllerhello = ControllerHello(view, model)
    
    #Adapter
    terminalStatusAdapter = TerminalStatusAdapter(view, model, subpub)
    terminalnicAdapter = TerminalNicAdapter(view, model, subpub)
    windowconfigAdapter = WindowConfigAdapter(view, model, subpub)
    terminalDataAdapter = TerminalDataAdapter(view, model, subpub)
    adapter_analyzedData = AdapterAnalyzedData(view, model, subpub)


    view.initializeWindow()
    # terminalController.registerEvents()
    rawDataController.registerEvents()
    menucontroller.registerEvents()
    controllerAnalyzedData.registerEvents()
    controllerhello.registerEvents()

    terminalStatusAdapter.subscribeModel_StatusSniffingData()
    terminalnicAdapter.subscribeModel_NicDataComboBox()
    windowconfigAdapter.subscribeModel_WindowConfiguration()
    terminalDataAdapter.subscribeModel_TerminalDataSniffing()
    adapter_analyzedData.subscribeModel_StateAnalysis()
    adapter_analyzedData.subscribeModel_DataAnalysis()
    adapter_analyzedData.subscribeModel_PackageAnalysis()

    model.initialize()

    app.exec()