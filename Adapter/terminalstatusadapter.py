class TerminalStatusAdapter:

    #constructor for SnifferAdapter
    def __init__(self, view, model, subpub):
        
        self._view = view
        self._model = model
        self._subpub = subpub

        self._sub_status_sniffing_data = None


    def subscribeModel_StatusSniffingData(self):
        #Subscribe StatusSniffingData
        print("SnifferAdapter: Subscribe PUBLISH_TOPIC_STATUSSNIFFINGDATA")
        self._sub_status_sniffing_data = self._subpub.subscribe(self._model.PUBLISH_TOPIC_STATUSSNIFFINGDATA, self.onNext)
    
    
    def unsubscribeModel_StatusSniffingData(self):
        #Unsubscribe PUBLISH_TOPIC_STATUSSNIFFINGDATA
        if self._sub_status_sniffing_data is not None:
            print("WindowConfigAdapter: Unsubscribe PUBLISH_TOPIC_STATUSSNIFFINGDATA")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_STATUSSNIFFINGDATA, self._sub_status_sniffing_data)


    def onNext(self, item):
        #Receiving a message after publisher publishes value
        if item is True:
            self._view.getTerminalBtnSniff().setText("Stop Sniffing")
            self._view.getTerminalBtnSniff().setToolTip("Stop Sniffing Network Data")
            self._view.getTerminalBtnSniff().setStatusTip("Stop Sniffing Network Data")
        elif item is False:
            self._view.getTerminalBtnSniff().setText("Start Sniffing")
            self._view.getTerminalBtnSniff().setToolTip("Start Sniffing Network Data")
            self._view.getTerminalBtnSniff().setStatusTip("Start Sniffing Network Data")

