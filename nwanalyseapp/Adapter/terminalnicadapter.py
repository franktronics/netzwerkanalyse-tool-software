class TerminalNicAdapter():

    #constructor for TerminalNicAdapter
    def __init__(self, view, model, subpub):
        
        self._view = view
        self._model = model

        self._subpub = subpub


    #Subscribe PUBLISH_TOPIC_TERMINAL_NIC
    def subscribeModel_NicDataComboBox(self):
        print("TerminalNicAdapter: Subscribe PUBLISH_TOPIC_TERMINAL_NIC")
        self._subscriptionTerminalNic = self._subpub.subscribe(self._model.PUBLISH_TOPIC_TERMINAL_NIC, self.onNext)


    #Unsubscribe PUBLISH_TOPIC_TERMINAL_NIC
    def unsubscribeModel_NicDataComboBox(self):
        if self._subscriptionTerminalNic != None:
            print("TerminalNicAdapter: Unsubscribe PUBLISH_TOPIC_TERMINAL_NIC")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_TERMINAL_NIC, self._subscriptionTerminalNic)


    #Receiving a message after publisher publishes value
    def onNext(self, item):
        self._view.getTerminalComboBoxNic().clear()
        self._view.getTerminalComboBoxNic().addItems(item)

