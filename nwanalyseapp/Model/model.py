from Model.analyzer import Analyzer
from Model.sniffer import Sniffer
from Model.snifferV2 import SnifferV2
from Model.storage import Storage
from Model.settings_view import Settings_View

class Model():
    

    #constructor for Model
    def __init__(self, subpub):
        #set Topics for Publish-Subscribe
        self.PUBLISH_TOPIC_STATUSSNIFFINGDATA = "statussniffingdata" 
        self.PUBLISH_TOPIC_TERMINAL_NIC = "nicterminal"
        self.PUBLISH_TOPIC_WINDOW_CONFIG = "windowconfig"
        self.PUBLISH_TOPIC_MODEL_DATA_SNIFFING = "modeldatasniffing"
        self.PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING = "adapterdatasniffing"
        

        self._analyzer = Analyzer()
        self._sniffer = SnifferV2(subpub, self.PUBLISH_TOPIC_MODEL_DATA_SNIFFING)
        self._storage = Storage()
        self._settings_view = Settings_View()
        
        self._subpub = subpub

    #Subscribe rawsnifferdata from sniffer
    def subscribeSniffer(self):
        print("Model: Subscribe PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING")
        self._subpub.subscribe(self.PUBLISH_TOPIC_MODEL_DATA_SNIFFING, self.onNextDataSniffing)

    #Sniffer: Detect OS
    def snifferDetectOS(self):
        retSniffData = self._sniffer.detectOS()


    #Sniffer: Detect Nic
    def snifferDetectNic(self):
        retSniffNicData = self._sniffer.detectNic()
        if self._settings_view.isWindowTerminal():
            self._subpub.publish(self.PUBLISH_TOPIC_TERMINAL_NIC, retSniffNicData)


    #Sniffer: change Sniffer State
    def snifferChangeSniffData(self, index_combobox):
        retStatusSniffData = self._sniffer.changeSniffData(index_combobox)
        self._subpub.publish(self.PUBLISH_TOPIC_STATUSSNIFFINGDATA, retStatusSniffData)

    #Sniffer: Stop Sniffing
    def snifferStopSniffData(self):
        retStatusSniffData = self._sniffer.stopSniffData()
        self._subpub.publish(self.PUBLISH_TOPIC_STATUSSNIFFINGDATA, retStatusSniffData)
        
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

    #Sniffing data: received from Sniffer
    def onNextDataSniffing(self, item):
        self._subpub.publish(self.PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING, item)


    def settingsViewInitializeWindow(self):
        pass

    def storageIsDataSaved(self):
        return self._storage.isStorageSaved()
    
    def storageClearStorage(self):
        self._storage.clearStorage()

    def storageIsStorageEmpty(self):
        return self._storage.isStorageEmpty()