class TerminalStatusAdapter():

    #constructor for SnifferAdapter
    def __init__(self, view, model, subpub):
        
        self._view = view
        self._model = model

        self._subpub = subpub


    #Subscribe StatusSniffingData
    def subscribeModel_StatusSniffingData(self):
        print("SnifferAdapter: Subscribe PUBLISH_TOPIC_STATUSSNIFFINGDATA")
        self._subscriptionStatusSniffingData = self._subpub.subscribe(self._model.PUBLISH_TOPIC_STATUSSNIFFINGDATA, self.onNext)
    
    
    #Unsubscribe PUBLISH_TOPIC_STATUSSNIFFINGDATA
    def unsubscribeModel_StatusSniffingData(self):
        if self._subscriptionStatusSniffingData != None:
            print("WindowConfigAdapter: Unsubscribe PUBLISH_TOPIC_STATUSSNIFFINGDATA")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_STATUSSNIFFINGDATA, self._subscriptionStatusSniffingData)


    #Receiving a message after publisher publishes value
    def onNext(self, item):
        if item == True:
            self._view.getTerminalBtnSniff().setText("Stop Sniffing")
            self._view.getTerminalBtnSniff().setToolTip("Stop Sniffing Network Data")
            self._view.getTerminalBtnSniff().setStatusTip("Stop Sniffing Network Data")
        elif item == False:
            self._view.getTerminalBtnSniff().setText("Start Sniffing")
            self._view.getTerminalBtnSniff().setToolTip("Start Sniffing Network Data")
            self._view.getTerminalBtnSniff().setStatusTip("Start Sniffing Network Data")

