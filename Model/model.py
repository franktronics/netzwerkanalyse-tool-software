from Model.storage import Storage
from Model.settings_view import Settings_View
from Model.utils import detectNic
from Model.analyser import NetworkAnalyserPort, NetworkAnalyser

class Model:
    PUBLISH_TOPIC_STATUSSNIFFINGDATA = "statussniffingdata"
    PUBLISH_TOPIC_TERMINAL_NIC = "nicterminal"
    PUBLISH_TOPIC_WINDOW_CONFIG = "windowconfig"
    PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING = "adapterdatasniffing"

    def __init__(self, subpub):
        self._storage = Storage()
        self._settings_view = Settings_View()
        
        self._subpub = subpub
        self._nics = []
        self._analyser: NetworkAnalyserPort = NetworkAnalyser()

        self.snifferDetectNic()

    def snifferDetectNic(self):
        # Detect available NICs
        if len(self._nics) == 0:
            self._nics = detectNic()
        if self._settings_view.isWindowTerminal():
            self._subpub.publish(self.PUBLISH_TOPIC_TERMINAL_NIC, self._nics)

    def snifferChangeSniffData(self, index_combobox):
        # Sniffer: change Sniffer State
        if self._analyser.is_running():
            self.snifferStopSniffData()
        else:
            analysis_id, timestamp, nic = self._analyser.record(
                self._nics[index_combobox],
                lambda _: self._subpub.publish(self.PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING, (analysis_id, timestamp, nic))
            )
            self._subpub.publish(self.PUBLISH_TOPIC_STATUSSNIFFINGDATA, False if analysis_id is None else True)

    def snifferStopSniffData(self):
        #Sniffer: Stop Sniffing
        self._analyser.stop_record()
        self._subpub.publish(self.PUBLISH_TOPIC_STATUSSNIFFINGDATA, False)
        
    #Storage: store collected sniffer data
    def storageStoreSniffingData(self):
        pass

    #Storage: Save Data to file
    def storageSaveSniffingData(self, filename):
        self._storage.saveSniffingData(filename)

    #Storage: Open file
    def storageOpenSniffingData(self, filename):
        self._storage.openSniffingData(filename)

    #return reference to view settings
    def settingsViewSetWindow(self, window_changed):
        retWindow = self._settings_view.setWindow(window_changed)
        self._subpub.publish(self.PUBLISH_TOPIC_WINDOW_CONFIG, retWindow)


    def settingsViewInitializeWindow(self):
        pass

    def storageIsDataSaved(self):
        return self._storage.isStorageSaved()
    
    def storageClearStorage(self):
        self._storage.clearStorage()

    def storageIsStorageEmpty(self):
        return self._storage.isStorageEmpty()