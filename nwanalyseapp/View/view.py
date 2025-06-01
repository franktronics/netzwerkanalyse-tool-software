from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar, QToolBar, QPushButton, QStatusBar, QLabel, QStackedWidget
from PyQt6.QtGui import QAction
from View.viewTable import ViewTable
from View.viewTerminal import ViewTerminal
from View.viewStatistics import ViewStatistics


class View(QMainWindow):

    #Constructor for creating the main_window
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Netzwerk-Analyse Tool")
        self.resize(600,400)

        self._createmenuBar()
        self.setMenuBar(self._menuBar)

        self._createToolbar()
        self.addToolBar(self._toolbar)

        self.stackedWidget = QStackedWidget()
        #self.initializeWindow()
        self.setCentralWidget(self.stackedWidget)

        self._createStatusBar()
        self.setStatusBar(self.statusBar)

        self.show()
    

    def getTerminalBtnSniff(self):
        return self._viewTerminal._btnSniff
    
    def getTerminalBtnSave(self):
        return self._viewTerminal._btnSave
    
    def getTerminalBtnLoad(self):
        return self._viewTerminal._btnLoad
    
    def getTerminalComboBoxNic(self):
        return self._viewTerminal._ComBoxadapter
    
    def getTableBtnLoadData(self):
        return self._viewTable._btnLoadData
    
    def getMenuActionNew(self):
        return self._actionNew
    
    def getMenuActionOpen(self):
        return self._actionOpen
    
    def getMenuActionSave(self):
        return self._actionSave
    
    def getMenuActionLoadProtocols(self):
        return self._actionloadProtocols
    
    def getMenuActionLoadTypedefs(self):
        return self._actionloadTypedefs
    
    def getMenuActionExit(self):
        return self._actionExit
    
    def getMenuActionViewTerminal(self):
        return self._actionViewTerminal
    
    def getMenuActionViewTable(self):
        return self._actionViewTable
    
    def getMenuActionViewStatistics(self):
        return self._actionViewStatistics
    
    def getMenuActionHelp(self):
        return self._actionHelp
    
    def getMenuActionAbout(self):
        return self._actionAbout


    #Create Widgets for mainWindow
    def initializeWindow(self):
        self._viewTable = ViewTable()
        self._viewTerminal = ViewTerminal()
        self._viewStatistics = ViewStatistics()

        self.stackedWidget.addWidget(self._viewTerminal)
        self.VIEWTERMINAL = 0
        self.stackedWidget.addWidget(self._viewTable)
        self.VIEWTABLE = 1
        self.stackedWidget.addWidget(self._viewStatistics)
        self.VIEWSTATISTICS = 2

        self.setWindow(self.VIEWTABLE)


    #Sets the center-App of the window 
    def setWindow(self, viewApp):
        self.stackedWidget.setCurrentIndex(viewApp)


    #Create _menuBar for main_window
    def _createmenuBar(self):

        self._menuBar = QMenuBar(self)


        self._createMenuItems()


        self._createActionsFile()
        self._createActionsEdit()
        self._createActionsView()
        self._createActionsHelp()


    #Create Menus for _menuBar
    def _createMenuItems(self):

        self._menuItemFile = QMenu("&File", self)
        self._menuItemEdit = QMenu("&Edit", self)
        self._menuItemView = QMenu("View", self)
        self._menuItemHelp = QMenu("&Help", self)


        self._menuBar.addMenu(self._menuItemFile)
        self._menuBar.addMenu(self._menuItemEdit)
        self._menuBar.addMenu(self._menuItemView)
        self._menuBar.addMenu(self._menuItemHelp)


    #Create Actions for MenuItem File
    def _createActionsFile(self):

        self._actionNew = QAction("&New", self)
        self._actionNew.setShortcut("Ctrl+N")
        self._actionNew.setToolTip("Create New File")
        self._actionNew.setStatusTip("Create New File")

        self._actionOpen = QAction("&Open Sniffing Data", self)
        self._actionOpen.setShortcut("Ctrl+O")
        self._actionOpen.setToolTip("Open a SniffingData-File")
        self._actionOpen.setStatusTip("Open a SniffingData-File")

        self._actionSave = QAction("&Save Sniffing Data", self)
        self._actionSave.setShortcut("Ctrl+S")
        self._actionSave.setToolTip("Save File")
        self._actionSave.setStatusTip("Save File")

        self._actionloadProtocols = QAction("&Load Protocols", self)
        # self._actionloadProtocols.setShortcut()
        self._actionloadProtocols.setToolTip("Load Protocols (Analyzing)")
        self._actionloadProtocols.setStatusTip("Load Protocols (Analyzing)")

        self._actionloadTypedefs = QAction("&Load Type-Definitions", self)
        # self._actionloadTypedefs.setShortcut()
        self._actionloadTypedefs.setToolTip("Load Type-Definitions for Visualization (Analyzing)")
        self._actionloadTypedefs.setStatusTip("Load Type-Definitions for Visualization (Analyzing)")

        self._actionExit = QAction("&Exit", self)
        self._actionExit.setToolTip("Exit application")
        self._actionExit.setStatusTip("Exit application")


        self._menuItemFile.addAction(self._actionNew)
        self._menuItemFile.addAction(self._actionOpen)
        self._menuItemFile.addAction(self._actionSave)
        self._menuItemFile.addSeparator()
        self._menuItemFile.addAction(self._actionloadProtocols)
        self._menuItemFile.addAction(self._actionloadTypedefs)
        self._menuItemFile.addSeparator()
        self._menuItemFile.addAction(self._actionExit)

    
    #Create Actions for MenuItem Edit
    def _createActionsEdit(self):
        pass


    #Create Actions for MenuItem View
    def _createActionsView(self):
        self._actionViewTable = QAction("&Table", self)
        self._actionViewTable.setToolTip("Show data in a table")
        self._actionViewTable.setStatusTip("Show data in a table")
        
        self._actionViewTerminal = QAction("&Terminal", self)
        self._actionViewTerminal.setToolTip("Show Terminal Data")
        self._actionViewTerminal.setStatusTip("Show Terminal Data")

        self._actionViewStatistics = QAction("&Statistics", self)
        self._actionViewStatistics.setToolTip("Show Statistics")
        self._actionViewStatistics.setStatusTip("Show Statistics")


        self._menuItemView.addAction(self._actionViewTable)
        self._menuItemView.addAction(self._actionViewTerminal)
        self._menuItemView.addAction(self._actionViewStatistics)

    
    #Create Actions for MenuItem Help
    def _createActionsHelp(self):

        self._actionHelp = QAction("&Help", self)
        self._actionHelp.setShortcut("Ctrl+H")
        self._actionHelp.setToolTip("Open Help")
        self._actionHelp.setStatusTip("Open Help")

        self._actionAbout = QAction("About...", self)
        self._actionAbout.setToolTip("information about the application")
        self._actionAbout.setStatusTip("information about the application")


        self._menuItemHelp.addAction(self._actionAbout)
        self._menuItemHelp.addAction(self._actionHelp)


    #Create Toolbar for fast accessible items
    def _createToolbar(self):

        self._toolbar = QToolBar()
        self._toolbar.addAction(self._actionViewTerminal)
        self._toolbar.addAction(self._actionViewTable)
        self._toolbar.addAction(self._actionViewStatistics)
        
        self._toolbar.setMovable(False)


    #Create statusbar for Tooltips and status
    def _createStatusBar(self):
        
        self.statusBar = QStatusBar(self)
        self.statusBar.showMessage("Ready", 3000)

        self.statusBarLabel = QLabel("")
        self.statusBar.addPermanentWidget(self.statusBarLabel)

    #Add Sniffing Data
    def addDataSniffing(self, item):
        self._viewTerminal.addDataSniffing(item)

    #show temporary message
    def showTemporaryMessage(self, message):
        self.statusBar.showMessage(message, 3000)