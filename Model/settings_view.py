class Settings_View():


    def __init__(self):

        
        #self.VIEWDEFAULT = 0
        self.VIEWTERMINAL = 0
        self.VIEWTABLE = 1
        self.VIEWSTATISTICS = 2

        self.initializeWindow()

        ##--------------------------------
        #states for analyzing table
        ##--------------------------------
        self.STATEDEFAULT = 0
        self.STATEDATABASE = 1
        self.STATEPACKAGE = 2
        self.STATESHOW = 3
        self.state = self.STATEDATABASE

        self._state_database()


    def initializeWindow(self):
        self.setWindow(self.VIEWTABLE)


    def isWindowTerminal(self):
        if self._window == self.VIEWTERMINAL:
            return True
        else:
            return False


    def setWindow(self, item):
        self._window = item
        return self._window


    def getWindow(self):
        return self._window
    

    #--------------------------------
    #states for analyzing table
    #--------------------------------
    def initializeState(self) -> int:
        self.state = self.STATEDATABASE
        self._state_database()

        return self.retState()

    
    def next(self) -> int:
        if self.state == self.STATEDEFAULT:
            self._state_default()
        elif self.state == self.STATEDATABASE:
            self._state_package()
        elif self.state == self.STATEPACKAGE:
            self._state_show()
        elif self.state == self.STATESHOW:
            pass

        return self.retState()

    def back(self) -> int:
        if self.state == self.STATEDEFAULT:
            self._state_default()
        elif self.state == self.STATEDATABASE:
            pass
        elif self.state == self.STATEPACKAGE:
            self._state_database()
        elif self.state == self.STATESHOW:
            self._state_package()

        return self.retState()

    
    def _state_database(self):
        self.state = self.STATEDATABASE

    def _state_package(self):
        self.state = self.STATEPACKAGE

    def _state_show(self):
        self.state = self.STATESHOW

    def _state_default(self):
        self.state = self.STATEDEFAULT

    def retState(self) -> int:
        return self.state

    