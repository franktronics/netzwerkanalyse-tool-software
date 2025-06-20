class TerminalDataAdapter:

    #constructor for TerminalDataAdapter
    def __init__(self, view, model, subpub):
        
        self._view = view
        self._model = model
        self._subpub = subpub

        self._sub_terminal_data_sniffing = None


    #Subscribe PUBLISH_TOPIC_TERMINAL_DATA_SNIFFING
    def subscribeModel_TerminalDataSniffing(self):
        print("TerminalNicAdapter: Subscribe PUBLISH_TOPIC_TERMINAL_DATA_SNIFFING")
        self._sub_terminal_data_sniffing = self._subpub.subscribe(self._model.PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING, self.onNext)


    #Unsubscribe PUBLISH_TOPIC_TERMINAL_DATA_SNIFFING
    def unsubscribeModel_TerminalDataSniffing(self):
        if self._sub_terminal_data_sniffing is not None:
            print("TerminalNicAdapter: Unsubscribe PUBLISH_TOPIC_TERMINAL_DATA_SNIFFING")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING, self._sub_terminal_data_sniffing)


    #Receiving a message after publisher publishes value
    def onNext(self, item: tuple[int, str, str]):
        self._view.addSniffingData(item)