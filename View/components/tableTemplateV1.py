from PyQt6.QtWidgets import QHeaderView, QTableView, QAbstractItemView
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
class TableTemplateV1():
    def __init__(self, list_columns):
        
        self.columns = list_columns
        self.itemmodel = QStandardItemModel()
        self.itemmodel.setHorizontalHeaderLabels(self.columns)

        self.table = QTableView()
        self.table.setModel(self.itemmodel)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)


    def getTable(self):
        return self.table


    def _addItems(self, item):
        items = [QStandardItem(str(data)) for data in item]
        self.itemmodel.appendRow(items)


    def addTestData(self, number):
        for row in range(number):
            items = [f"{row},{col}" for col in range(self.itemmodel.columnCount())]
            self._addItems(items)


    def clear(self):
        self.itemmodel.clear()
        self.itemmodel.setHorizontalHeaderLabels(self.columns)
    

    def addData(self, data):
        self.clear()
        for item in data:
            if len(item) != len(self.columns):
                raise ValueError(f"Tuple length {len(item)} does not match number of columns {len(self.columns)}")
            self._addItems(item)


    def item(self, row:int, col:int) -> str:
        return self.itemmodel.item(row, col).text()