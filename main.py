from PyQt6.QtWidgets import QApplication

from View.view_V2 import ViewV2
from Model.model import Model

# Controller
from Controller.menucontroller import MenuController
from Controller.rawdata_controller import RawDataController
from Controller.controller_analyzedData import ControllerAnalyzedData
from Controller.controller_hello import ControllerHello

#Adapter
from Adapter.adapter_rawdata import AdapterRawData
from Adapter.windowconfigadapter import WindowConfigAdapter
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
    rawDataController = RawDataController(view, model)
    menucontroller = MenuController(view, model)
    controllerAnalyzedData = ControllerAnalyzedData(view, model)
    controllerhello = ControllerHello(view, model)
    
    #Adapter
    adapter_rawData = AdapterRawData(view, model, subpub)
    windowconfigAdapter = WindowConfigAdapter(view, model, subpub)
    adapter_analyzedData = AdapterAnalyzedData(view, model, subpub)


    view.initializeWindow()
    rawDataController.registerEvents()
    menucontroller.registerEvents()
    controllerAnalyzedData.registerEvents()
    controllerhello.registerEvents()

    windowconfigAdapter.subscribeModel_WindowConfiguration()
    adapter_rawData.subscribeModel_RawData_Nic()
    adapter_rawData.subscribeModel_RawData_SniffingData()
    adapter_rawData.subscribeModel_RawData_StatusSniffingData()
    adapter_analyzedData.subscribeModel_StateAnalysis()
    adapter_analyzedData.subscribeModel_DataAnalysis()
    adapter_analyzedData.subscribeModel_PackageAnalysis()
    adapter_analyzedData.subscribeModel_showAnalysis()

    model.initialize()

    app.exec()