#Outdated - same functions in adapter_rawdata


class TerminalNicAdapter():

    #constructor for TerminalNicAdapter
    def __init__(self, view, model, subpub):
        
        self._view = view
        self._model = model
        self._subpub = subpub

        self._sub_terminal_nic_adapter = None


    #Subscribe PUBLISH_TOPIC_TERMINAL_NIC
    def subscribeModel_NicDataComboBox(self):
        print("TerminalNicAdapter: Subscribe PUBLISH_TOPIC_TERMINAL_NIC")
        self._sub_terminal_nic_adapter = self._subpub.subscribe(self._model.PUBLISH_TOPIC_TERMINAL_NIC, self.onNext)


    #Unsubscribe PUBLISH_TOPIC_TERMINAL_NIC
    def unsubscribeModel_NicDataComboBox(self):
        if self._sub_terminal_nic_adapter is not None:
            print("TerminalNicAdapter: Unsubscribe PUBLISH_TOPIC_TERMINAL_NIC")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_TERMINAL_NIC, self._sub_terminal_nic_adapter)


    #Receiving a message after publisher publishes value
    def onNext(self, item):
        self._view.setRawDataNics(item)

