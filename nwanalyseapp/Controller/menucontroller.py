from PyQt6.QtWidgets import QFileDialog, QMessageBox

class MenuController():

    #Constructor for MenuController
    def __init__(self, view, model):
        self._view = view
        self._model = model

    #Register Events for view-components
    def registerEvents(self):
        #self._view.getMenuActionNew().triggered.connect(self._actionPerformedNew)
        # self._view.getMenuActionOpen().triggered.connect(self._actionPerformedOpen)
        self._view.getMenuActionExport().triggered.connect(self._actionPerformedExport)
        self._view.getMenuActionLoadProtocols().triggered.connect(self._actionPerformedLoadProtocols)
        self._view.getMenuActionLoadTypedefs().triggered.connect(self._actionPerformedLoadTypedefs)
        self._view.getMenuActionExit().triggered.connect(self._actionPerformedExit)

        self._view.getMenuActionViewRawData().triggered.connect(self._actionPerformedRawData)
        self._view.getMenuActionViewTable().triggered.connect(self._actionPerformedViewTable)
        self._view.getMenuActionViewStatistics().triggered.connect(self._actionPerformedViewStatistics)

        self._view.getMenuActionHelp().triggered.connect(self._actionPerformedHelp)
        self._view.getMenuActionAbout().triggered.connect(self._actionPerformedAbout)
    

    # #Action for MenuItem-Action New
    # def _actionPerformedNew(self):
    #     self._model.snifferStopSniffData()
    #     while True:
    #         if self._model.storageIsDataSaved():
    #             self._model.storageClearStorage()

    #             self._view.showTemporaryMessage("New workspace...")
    #             break
    #         else:
    #             print("Can't create a new workspace as Data isn't saved yet")
    #             msgBox = QMessageBox(self._view)
    #             msgBox.setWindowTitle("Save Sniffing Data")
    #             msgBox.setText("The data has been modified.")
    #             msgBox.setInformativeText("Do you want to save your changes?")
    #             msgBox.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
    #             msgBox.setDefaultButton(QMessageBox.StandardButton.Save)

    #             ret = msgBox.exec()

    #             if ret == QMessageBox.StandardButton.Save:
    #                 print("Save clicked")
    #                 self._actionPerformedSave()
    #             elif ret == QMessageBox.StandardButton.Discard:
    #                 print("Discard clicked")
    #                 self._model.storageClearStorage()
    #             elif ret == QMessageBox.StandardButton.Cancel:
    #                 print("Cancel clicked")
    #                 break


    #Action for MenuItem-Action Open
    # def _actionPerformedOpen(self):
    #     self._model.stop_record()
                
    #     #execute filedialog
    #     filename = QFileDialog.getOpenFileName(self._view, "Open Sniffing data", "", "Text files (*.txt)")
    #     print("Open: " + str(filename))
                
    #     #get the filename without the filter
    #     filename = filename[0]
    #     if filename != '':
    #         self._model.storageOpenSniffingData(filename)
        
        


    #Action for Saving Sniffing Data
    def _actionPerformedExport(self):
        #self._model.stop_record()

       
        #execute filedialog
        filename = QFileDialog.getSaveFileName(self._view, "Save Sniffing data", "", "Text files (*.txt)")
        print("Save: " + str(filename))
            
        #get the filename without the filter
        filename = filename[0]
        if filename != '':
            #self._model.exportData(filename) TODO
            pass

    
    #Action for MenuItem-Action "Load Protocols"
    def _actionPerformedLoadProtocols(self):
        pass


    #Action for MenuItem-Action "Load Typedefs"
    def _actionPerformedLoadTypedefs(self):
        pass


    #Action for MenuItem-Action Exit
    def _actionPerformedExit(self):
        #self._model.stop_record()
        pass

    #Action for MenuItem-Action ViewRawData
    def _actionPerformedRawData(self):
        self._view.setWindow(self._view.VIEWRAWDATA)
        
        # self._model.settingsViewSetWindow(self._view.VIEWRAWDATA)
        # self._model.snifferDetectNic()

    #Action for MenuItem-Action ViewList
    def _actionPerformedViewTable(self):
        self._view.setWindow(self._view.VIEWTABLE)
        
        # self._model.settingsViewSetWindow(self._view.VIEWTABLE)
        # self._model.snifferStopSniffData()
    

    #Action for MenuItem-Action ViewStatistics
    def _actionPerformedViewStatistics(self):
        self._view.setWindow(self._view.VIEWSTATISTICS)
        
        # self._model.settingsViewSetWindow(self._view.VIEWSTATISTICS)
        # self._model.snifferStopSniffData()


    #Action for MenuItem-Action Help
    def _actionPerformedHelp(self):
        pass


    #Action for MenuItem-Action About
    def _actionPerformedAbout(self):
        pass

