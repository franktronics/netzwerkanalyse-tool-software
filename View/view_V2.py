from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar, QToolBar, QPushButton, QStatusBar, QLabel, QStackedWidget
from PyQt6.QtGui import QAction
from View.view_RawDataV2 import ViewRawDataV2
from View.viewStatistics import ViewStatistics
from View.view_analyzedData import ViewAnalyzedData
from View.view_hello import ViewHello

from PyQt6.QtGui import QIcon


class ViewV2(QMainWindow):

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
    

    def getRawDataBtnStartSniffing(self):
        return self._viewRawData._btnStartSniffing
    
    def getRawDataBtnStopSniffing(self):
        return self._viewRawData._btnStopSniffing
    
    def getRawDataBtnExport(self):
        return self._viewRawData._btnExport
    
    def getRawDataTable(self):
        return self._viewRawData.table
    
    # def getRawDataBtnLoad(self):
    #     return self._viewRawData._btnLoad
    
    def getRawDataComboBoxNic(self):
        return self._viewRawData._ComBoxadapter
    
    def getRawDataBtnRefreshNic(self):
        return self._viewRawData._btnRefreshNic
    
    def getAnalyzedDataBtnLoadData(self):
        return self._viewanalyzedData._btnLoadData
    
    # def getMenuActionNew(self):
    #     return self._actionNew
    
    # def getMenuActionOpen(self):
    #     return self._actionOpen
    
    def getMenuActionExport(self):
        return self._actionExport
    
    def getMenuActionLoadProtocols(self):
        return self._actionloadProtocols
    
    def getMenuActionLoadTypedefs(self):
        return self._actionloadTypedefs
    
    def getMenuActionExit(self):
        return self._actionExit
    
    def getMenuActionViewRawData(self):
        return self._actionViewRawData
    
    def getMenuActionViewAnalyzedData(self):
        return self._actionViewAnalyzedData
    
    def getMenuActionViewStatistics(self):
        return self._actionViewStatistics
    
    def getMenuActionHelp(self):
        return self._actionHelp
    
    def getMenuActionAbout(self):
        return self._actionAbout

    def setRawDataNics(self, nics):
        return self._viewRawData.updateNics(nics)

    #Create Widgets for mainWindow
    def initializeWindow(self):
        self._viewanalyzedData = ViewAnalyzedData()
        self._viewRawData = ViewRawDataV2()
        self._viewStatistics = ViewStatistics()
        self._viewHello = ViewHello()

        self.stackedWidget.addWidget(self._viewRawData)
        self.VIEWRAWDATA = 0
        self.stackedWidget.addWidget(self._viewanalyzedData)
        self.VIEWANALYZEDDATA = 1
        self.stackedWidget.addWidget(self._viewStatistics)
        self.VIEWSTATISTICS = 2
        self.stackedWidget.addWidget(self._viewHello)
        self.VIEWHELLO = 3

        self.setWindow(self.VIEWHELLO)


    #Sets the center-App of the window 
    def setWindow(self, viewApp):
        self.stackedWidget.setCurrentIndex(viewApp)


    #Create _menuBar for main_window
    def _createmenuBar(self):

        self._menuBar = QMenuBar(self)


        self._createMenuItems()


        self._createActionsFile()
        self._createActionsEdit()
        self._createActionsAnalysis()
        self._createActionsView()
        self._createActionsHelp()


    #Create Menus for _menuBar
    def _createMenuItems(self):

        self._menuItemFile = QMenu("&File", self)
        self._menuItemEdit = QMenu("&Edit", self)
        self._menuItemAnalysis = QMenu("&Analysis", self)
        self._menuItemView = QMenu("View", self)
        self._menuItemHelp = QMenu("&Help", self)


        self._menuBar.addMenu(self._menuItemFile)
        self._menuBar.addMenu(self._menuItemEdit)
        self._menuBar.addMenu(self._menuItemAnalysis)
        self._menuBar.addMenu(self._menuItemView)
        self._menuBar.addMenu(self._menuItemHelp)


    #Create Actions for MenuItem File
    def _createActionsFile(self):

        # self._actionNew = QAction("&New", self)
        # self._actionNew.setShortcut("Ctrl+N")
        # self._actionNew.setToolTip("Create New File")
        # self._actionNew.setStatusTip("Create New File")

        # self._actionOpen = QAction("&Open Sniffing Data", self)
        # self._actionOpen.setShortcut("Ctrl+O")
        # self._actionOpen.setToolTip("Open a SniffingData-File")
        # self._actionOpen.setStatusTip("Open a SniffingData-File")

        self._actionExport = QAction("&Export Sniffing Data", self)
        self._actionExport.setShortcut("Ctrl+E")
        self._actionExport.setToolTip("Export data to File")
        self._actionExport.setStatusTip("Export data to File")

        self._actionloadProtocols = QAction("Load Protocols", self)
        # self._actionloadProtocols.setShortcut()
        self._actionloadProtocols.setToolTip("Load Protocols (Analyzing)")
        self._actionloadProtocols.setStatusTip("Load Protocols (Analyzing)")

        self._actionloadTypedefs = QAction("Load Type-Definitions", self)
        # self._actionloadTypedefs.setShortcut()
        self._actionloadTypedefs.setToolTip("Load Type-Definitions for Visualization (Analyzing)")
        self._actionloadTypedefs.setStatusTip("Load Type-Definitions for Visualization (Analyzing)")

        self._actionExit = QAction("&Exit", self)
        self._actionExit.setToolTip("Exit application")
        self._actionExit.setStatusTip("Exit application")


        # self._menuItemFile.addAction(self._actionNew)
        # self._menuItemFile.addAction(self._actionOpen)
        self._menuItemFile.addAction(self._actionExport)
        self._menuItemFile.addSeparator()
        self._menuItemFile.addAction(self._actionloadProtocols)
        self._menuItemFile.addAction(self._actionloadTypedefs)
        self._menuItemFile.addSeparator()
        self._menuItemFile.addAction(self._actionExit)

    
    #Create Actions for MenuItem Edit
    def _createActionsEdit(self):
        pass
    
    
    def _createActionsAnalysis(self):
        self._actionAnalysisDelete = QAction("Delete record", self)
        self._actionAnalysisDelete.setToolTip("Delete a record from the database")
        self._actionAnalysisDelete.setStatusTip("Delete a record from the database")

        self._menuItemAnalysis.addAction(self._actionAnalysisDelete)




    #Create Actions for MenuItem View
    def _createActionsView(self):
        self._actionViewAnalyzedData = QAction("&AnalyzedData", self)
        self._actionViewAnalyzedData.setToolTip("Show data in a AnalyzedData")
        self._actionViewAnalyzedData.setStatusTip("Show data in a AnalyzedData")
        
        self._actionViewRawData = QAction("&RawData", self)
        self._actionViewRawData.setToolTip("Show Raw Data")
        self._actionViewRawData.setStatusTip("Show Raw Data")

        self._actionViewStatistics = QAction("&Statistics", self)
        self._actionViewStatistics.setToolTip("Show Statistics")
        self._actionViewStatistics.setStatusTip("Show Statistics")


        self._menuItemView.addAction(self._actionViewAnalyzedData)
        self._menuItemView.addAction(self._actionViewRawData)
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
        self._toolbar.addAction(self._actionViewRawData)
        self._toolbar.addAction(self._actionViewAnalyzedData)
        self._toolbar.addAction(self._actionViewStatistics)
        
        self._toolbar.setMovable(False)


    #Create statusbar for Tooltips and status
    def _createStatusBar(self):
        
        self.statusBar = QStatusBar(self)
        self.statusBar.showMessage("Ready", 3000)

        self.statusBarLabel = QLabel("")
        self.statusBar.addPermanentWidget(self.statusBarLabel)

    #Add Sniffing Data
    def addSniffingData(self, item):
        self._viewRawData.addSniffingData(item)

    #show temporary message
    def showTemporaryMessage(self, message):
        self.statusBar.showMessage(message, 3000)

    
    def activateAnalysis(self):
        self._actionAnalysisDelete.setDisabled(False)


    def deactivateAnalysis(self):
        self._actionAnalysisDelete.setDisabled(True)

    def analyzedDataSetState(self, state:int):
        self._viewanalyzedData.setState(state)

    def analyzedData_loadAnalysis(self, data):
        self._viewanalyzedData.loadAnalysis(data)

    def analyzedData_loadPackages(self, data):
        self._viewanalyzedData.loadPackages(data)

    def analyzedData_showAnalysis(self, data):
        self._viewanalyzedData.showAnalysis(data)