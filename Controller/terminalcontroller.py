from PyQt6.QtWidgets import QFileDialog, QMessageBox

class TerminalController:

    #constructor for BtnController
    def __init__(self, view, model):
        
        self._view = view
        self._model = model


    #Register Events for view-components
    def registerEvents(self):
        self._view.getTerminalBtnSniff().clicked.connect(self._perfom_sniffing)
        self._view.getTerminalComboBoxNic().currentIndexChanged.connect(self._actionPerformedCombobox)
        self._view.getTerminalBtnSave().clicked.connect(self._actionPerformedSave)
        self._view.getTerminalBtnLoad().clicked.connect(self._actionPerformedLoad)


    def _perfom_sniffing(self):
        # Start or stop sniffing based on the state of the analyser
        index_combobox = self._view.getTerminalComboBoxNic().currentIndex()
        self._model.snifferChangeSniffData(index_combobox)


    #Action for ComboBox
    def _actionPerformedCombobox(self):
        self._model.snifferStopSniffData()


    #Action for Saving Sniffing Data
    def _actionPerformedSave(self):
        self._model.snifferStopSniffData()

        if self._model.storageIsStorageEmpty():
            msgBox = QMessageBox(self._view)
            msgBox.setWindowTitle("Save Sniffing data")
            msgBox.setText("No data available")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Ok)

            msgBox.exec()

        else:
            #execute filedialog
            filename = QFileDialog.getSaveFileName(self._view, "Save Sniffing data", "", "Text files (*.txt)")
            print("Save: " + str(filename))
            
            #get the filename without the filter
            filename = filename[0]
            if filename != '':
                self._model.storageSaveSniffingData(filename)

    
    #Action for Loading Sniffing Data
    def _actionPerformedLoad(self):
        self._model.snifferStopSniffData()
        while True:
            if self._model.storageIsDataSaved():
                #execute filedialog
                filename = QFileDialog.getOpenFileName(self._view, "Open Sniffing data", "", "Text files (*.txt)")
                print("Open: " + str(filename))
                
                #get the filename without the filter
                filename = filename[0]
                if filename != '':
                    self._model.storageOpenSniffingData(filename)
                break
            else:
                print("Can't open a new file as Data isn't saved yet")
                msgBox = QMessageBox(self._view)
                msgBox.setWindowTitle("Open Sniffing data")
                msgBox.setText("The data has been modified.")
                msgBox.setInformativeText("Do you want to save your changes?")
                msgBox.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
                msgBox.setDefaultButton(QMessageBox.StandardButton.Save)

                ret = msgBox.exec()

                if ret == QMessageBox.StandardButton.Save:
                    print("Save clicked")
                    self._actionPerformedSave()
                elif ret == QMessageBox.StandardButton.Discard:
                    print("Discard clicked")
                    self._model.storageClearStorage()
                elif ret == QMessageBox.StandardButton.Cancel:
                    print("Cancel clicked")
                    break

        


# self.storage = []
# filename = QFileDialog.getOpenFileName(self._view, "Open Sniffing data", "", "Text files (*.txt)")
# print("Open: " + str(filename))
# file = open(filename)
# self.storage = file.read().splitlines()
        
