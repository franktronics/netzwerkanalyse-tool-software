class AdapterRawData():

    #constructor for AdapterRawData
    def __init__(self, view, model, subpub):
        
        self._view = view
        self._model = model
        self._subpub = subpub

        self._sub_rawdata_sniffing = None
        self._sub_rawdata_nic_adapter = None
        self._sub_rawdata_status_sniffing_data = None


    #Subscribe PUBLISH_TOPIC_RAWDATA_SNIFFINGDATA
    def subscribeModel_RawData_SniffingData(self):
        print("AdapterRawData: Subscribe PUBLISH_TOPIC_RAWDATA_SNIFFINGDATA")
        self._sub_rawdata_sniffing = self._subpub.subscribe(self._model.PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING, self.onNext_RawData_SniffingData)


    #Unsubscribe PUBLISH_TOPIC_RAWDATA_SNIFFINGDATA
    def unsubscribeModel_RawData_SniffingData(self):
        if self._sub_rawdata_sniffing is not None:
            print("AdapterRawData: Unsubscribe PUBLISH_TOPIC_RAWDATA_SNIFFINGDATA")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING, self._sub_rawdata_sniffing)


    #Receiving a message after publisher publishes value
    def onNext_RawData_SniffingData(self, item: tuple[int, str, str]):
        self._view.addSniffingData(item)

#---------------------------------------------------------------------
    
    #Subscribe PUBLISH_TOPIC_RAWDATA_NIC
    def subscribeModel_RawData_Nic(self):
        print("AdapterRawData: Subscribe PUBLISH_TOPIC_RAWDATA_NIC")
        self._sub_rawdata_nic_adapter = self._subpub.subscribe(self._model.PUBLISH_TOPIC_RAWDATA_NIC, self.onNext_RawData_Nic)


    #Unsubscribe PUBLISH_TOPIC_TERMINAL_NIC
    def unsubscribeModel_RawData_Nic(self):
        if self._sub_rawdata_nic_adapter is not None:
            print("AdapterRawData: Unsubscribe PUBLISH_TOPIC_RAWDATA_NIC")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_RAWDATA_NIC, self._sub_rawdata_nic_adapter)


    #Receiving a message after publisher publishes value
    def onNext_RawData_Nic(self, item):
        self._view.setRawDataNics(item)

#---------------------------------------------------------------------

    def subscribeModel_RawData_StatusSniffingData(self):
        #Subscribe PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA
        print("AdapterRawData: Subscribe PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA")
        self._sub_rawdata_status_sniffing_data = self._subpub.subscribe(self._model.PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA, self.onNext_RawData_StatusSniffingData)
    
    
    def unsubscribeModel_RawData_StatusSniffingData(self):
        #Unsubscribe PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA
        if self._sub_rawdata_status_sniffing_data is not None:
            print("AdapterRawData: Unsubscribe PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA, self._sub_rawdata_status_sniffing_data)


    def onNext_RawData_StatusSniffingData(self, item):
        #Receiving a message after publisher publishes value
        # if item is True:
        #     self._view.getTerminalBtnSniff().setText("Stop Sniffing")
        #     self._view.getTerminalBtnSniff().setToolTip("Stop Sniffing Network Data")
        #     self._view.getTerminalBtnSniff().setStatusTip("Stop Sniffing Network Data")
        # elif item is False:
        #     self._view.getTerminalBtnSniff().setText("Start Sniffing")
        #     self._view.getTerminalBtnSniff().setToolTip("Start Sniffing Network Data")
        #     self._view.getTerminalBtnSniff().setStatusTip("Start Sniffing Network Data")
        pass