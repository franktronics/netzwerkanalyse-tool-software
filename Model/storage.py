class Storage:

    #Constructor for Storage
    def __init__(self):
        self._dataSaved:bool = True
        self._storageData = []

    #returns state (empty:1/notempty:0) of storageData
    def isStorageEmpty(self):
        if len(self._storageData) == 0:
            return True
        else:
            return False

    #returns state of dataSaved
    def isStorageSaved(self) -> bool:
        return self._dataSaved
    
    #sets DataSaved to false --> if new packets are tracked
    def setStorageSavedFalse(self):
        self._dataSaved = False

    #sets DataSaved to true --> if every file is saved (internal)
    def _setStorageSavedTrue(self):
        self._dataSaved = True

    #Stores sniffing data in a list
    def storeSniffingData(self, sniffing_data):
        self._storageData.append(sniffing_data)
        self.setStorageSavedFalse()

    #Save sniffingdata
    def saveSniffingData(self, filename):
        print("Save Sniffing Data to File")
        
        with open(filename, 'w') as file:
            for line in self._storageData:
                file.write(f"{line}\n")

        self._setStorageSavedTrue()

    
    #Open sniffingdata
    def openSniffingData(self, filename):
        print("Open SniffingData-File")
        
        self.clearStorage()
        with open(filename, 'r') as file:
            self._storageData = file.read().splitlines()

        self._setStorageSavedTrue()

    #Clear Storage
    def clearStorage(self):
        self._storageData.clear()
        self._setStorageSavedTrue() #default-setting






# self.storage = []
# filename = QFileDialog.getOpenFileName(self._view, "Open Sniffing data", "", "Text files (*.txt)")
# print("Open: " + str(filename))
# file = open(filename)
# self.storage = file.read().splitlines()