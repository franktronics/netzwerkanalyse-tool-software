class WindowConfigAdapter():

    #constructor for WindowConfigAdapter
    def __init__(self, view, model, subpub):
        
        self._view = view
        self._model = model

        self._subpub = subpub


    #Subscribe PUBLISH_TOPIC_WINDOW_CONFIG
    def subscribeModel_WindowConfiguration(self):
        print("WindowConfigAdapter: Subscribe PUBLISH_TOPIC_WINDOW_CONFIG")
        self._subscriptionWindowConfiguration = self._subpub.subscribe(self._model.PUBLISH_TOPIC_WINDOW_CONFIG, self.onNext)
    

    #Unsubscribe PUBLISH_TOPIC_WINDOW_CONFIG
    def unsubscribeModel_WindowConfiguration(self):
        if self._subscriptionWindowConfiguration != None:
            print("WindowConfigAdapter: Unsubscribe PUBLISH_TOPIC_WINDOW_CONFIG")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_WINDOW_CONFIG, self._subscriptionWindowConfiguration)


    #Receiving a message after publisher publishes value
    def onNext(self, item):
        self._view.setWindow(item)

