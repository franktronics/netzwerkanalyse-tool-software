class TerminalDataAdapter():

    #constructor for TerminalDataAdapter
    def __init__(self, view, model, subpub):
        
        self._view = view
        self._model = model

        self._subpub = subpub


    #Subscribe PUBLISH_TOPIC_TERMINAL_DATA_SNIFFING
    def subscribeModel_TerminalDataSniffing(self):
        print("TerminalNicAdapter: Subscribe PUBLISH_TOPIC_TERMINAL_DATA_SNIFFING")
        self._subscriptionTerminalDataSniffing = self._subpub.subscribe(self._model.PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING, self.onNext)


    #Unsubscribe PUBLISH_TOPIC_TERMINAL_DATA_SNIFFING
    def unsubscribeModel_TerminalDataSniffing(self):
        if self._subscriptionTerminalDataSniffing != None:
            print("TerminalNicAdapter: Unsubscribe PUBLISH_TOPIC_TERMINAL_DATA_SNIFFING")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING, self._subscriptionTerminalDataSniffing)


    #Receiving a message after publisher publishes value
    def onNext(self, item):
        self._view.addDataSniffing(item)