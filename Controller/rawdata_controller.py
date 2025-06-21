from PyQt6.QtWidgets import QFileDialog, QMessageBox

class RawDataController():

    #constructor for BtnController
    def __init__(self, view, model):
        
        self._view = view
        self._model = model


    #Register Events for view-components
    def registerEvents(self):
        self._view.getRawDataBtnStartSniffing().clicked.connect(self._actionPerformedStartSniffing)
        self._view.getRawDataBtnStopSniffing().clicked.connect(self._actionPerformedStopSniffing)
        self._view.getRawDataComboBoxNic().currentIndexChanged.connect(self._actionPerformedCombobox)
        self._view.getRawDataBtnRefreshNic().clicked.connect(self._actionPerformedBtnRefreshNic)
        self._view.getRawDataBtnExport().clicked.connect(self._actionPerformedExport)


    #Action for ButtonStartSniffing
    def _actionPerformedStartSniffing(self):
        #getting the nic as a string (not an index!!)
        str_combobox = self._view.getRawDataComboBoxNic().itemText(self._view.getRawDataComboBoxNic().currentIndex())
        self._model.snifferStartSniffData(str_combobox)


    #Action for ButtonStopSniffing
    def _actionPerformedStopSniffing(self):
        self._model.snifferStopSniffData()


    #Action for ComboBox
    def _actionPerformedCombobox(self):
        self._model.snifferStopSniffData()


    def _actionPerformedBtnRefreshNic(self):
        self._model.snifferDetectNic()
        # self._view.setRawDataNics(nics)


    #Action for Saving Sniffing Data
    def _actionPerformedExport(self):
        self._model.snifferStopSniffData()

       
        #execute filedialog
        filename = QFileDialog.getSaveFileName(self._view, "Save Sniffing data", "", "Text files (*.txt)")
        print("Save: " + str(filename))
            
        #get the filename without the filter
        filename = filename[0]
        if filename != '':
            #self._model.exportData(filename) TODO
            pass

