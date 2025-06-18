class Settings_View():


    def __init__(self):

        
        #self.VIEWDEFAULT = 0
        self.VIEWTERMINAL = 0
        self.VIEWTABLE = 1
        self.VIEWSTATISTICS = 2

        self.initializeWindow()


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