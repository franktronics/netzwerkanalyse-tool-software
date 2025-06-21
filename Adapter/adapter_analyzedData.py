

class AdapterAnalyzedData():
    
    #constructor for AdapterAnalyzedData
    def __init__(self, view, model, subpub):
        
        self._view = view
        self._model = model
        self._subpub = subpub

        self._sub_analyzedData_state = None
        self._sub_analyzedData_analysis = None
        self._sub_analyzedData_package = None
        self._sub_analyzedData_show = None

    #Subscribe PUBLISH_TOPIC_ANALYZEDDATA_STATE
    def subscribeModel_StateAnalysis(self):
        print("AdapterState: Subscribe PUBLISH_TOPIC_ANALYZEDDATA_STATE")
        self._sub_analyzedData_state = self._subpub.subscribe(self._model.PUBLISH_TOPIC_ANALYZEDDATA_STATE, self.onNextState)

    #Unsubscribe PUBLISH_TOPIC_ANALYZEDDATA_STATE
    def unsubscribeModel_StateAnalysis(self):
        if self._sub_analyzedData_state is not None:
            print("AdapterState: Unsubscribe PUBLISH_TOPIC_ANALYZEDDATA_STATE")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_ANALYZEDDATA_STATE, self._sub_analyzedData_state)

    #Receiving a message after publisher publishes value
    def onNextState(self, item: int):
        self._view.analyzedDataSetState(item)



    #Subscribe PUBLISH_TOPIC_ANALYZEDDATA_ANALYSIS
    def subscribeModel_DataAnalysis(self):
        print("AdapterState: Subscribe PUBLISH_TOPIC_ANALYZEDDATA_ANALYSIS")
        self._sub_analyzedData_analysis = self._subpub.subscribe(self._model.PUBLISH_TOPIC_ANALYZEDDATA_ANALYSIS, self.onNextDataAnalysis)

    #Unsubscribe PUBLISH_TOPIC_ANALYZEDDATA_ANALYSIS
    def unsubscribeModel_DataAnalysis(self):
        if self._sub_analyzedData_analysis is not None:
            print("AdapterState: Unsubscribe PUBLISH_TOPIC_ANALYZEDDATA_ANALYSIS")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_ANALYZEDDATA_ANALYSIS, self._sub_analyzedData_analysis)

    #Receiving a message after publisher publishes value
    def onNextDataAnalysis(self, item):
        self._view.analyzedData_loadAnalysis(item)

    
    
    #Subscribe PUBLISH_TOPIC_ANALYZEDDATA_PACKAGE
    def subscribeModel_PackageAnalysis(self):
        print("AdapterState: Subscribe PUBLISH_TOPIC_ANALYZEDDATA_PACKAGE")
        self._sub_analyzedData_package = self._subpub.subscribe(self._model.PUBLISH_TOPIC_ANALYZEDDATA_PACKAGE, self.onNextPackageAnalysis)

    #Unsubscribe PUBLISH_TOPIC_ANALYZEDDATA_PACKAGE
    def unsubscribeModel_PackageAnalysis(self):
        if self._sub_analyzedData_package is not None:
            print("AdapterState: Unsubscribe PUBLISH_TOPIC_ANALYZEDDATA_PACKAGE")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_ANALYZEDDATA_PACKAGE, self._sub_analyzedData_package)

    #Receiving a message after publisher publishes value
    def onNextPackageAnalysis(self, item):
        self._view.analyzedData_loadPackages(item)


    
    #Subscribe PUBLISH_TOPIC_ANALYZEDDATA_SHOW
    def subscribeModel_showAnalysis(self):
        print("AdapterState: Subscribe PUBLISH_TOPIC_ANALYZEDDATA_SHOW")
        self._sub_analyzedData_show = self._subpub.subscribe(self._model.PUBLISH_TOPIC_ANALYZEDDATA_SHOW, self.onNextshowAnalysis)

    #Unsubscribe 
    def unsubscribeModel_showAnalysis(self):
        if self._sub_analyzedData_show is not None:
            print("AdapterState: Unsubscribe PUBLISH_TOPIC_ANALYZEDDATA_SHOW")
            self._subpub.unsubscribe(self._model.PUBLISH_TOPIC_ANALYZEDDATA_SHOW, self._sub_analyzedData_show)

    #Receiving a message after publisher publishes value
    def onNextshowAnalysis(self, item: int):
        self._view.analyzedData_showAnalysis(item)