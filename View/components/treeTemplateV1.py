from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class TreeTemplateV1():

    def __init__(self):
        
        self.itemmodel = QStandardItemModel()
        self.itemmodel.setHorizontalHeaderLabels(["Analysis"])

        self.treeView = QTreeView()
        self.treeView.setModel(self.itemmodel)
        self.treeView.setHeaderHidden(False)
        self.treeView.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)

    def getTree(self):
        return self.treeView

    def clear(self):
        self.itemmodel.clear()
        self.itemmodel.setHorizontalHeaderLabels(["Analysis"])


    def showData(self, data : dict[str, dict[str, any]]):
        self.clear()
        self._addDataRecursive(data, self.itemmodel.invisibleRootItem())
        

    def _addDataRecursive(self, data, parentItem:QStandardItem):
        if isinstance(data, dict):
            if set(data.keys()).issubset({"value", "description"}):
                if "value" in data:
                    value_item = QStandardItem(f"value: {data['value']}")
                    parentItem.appendRow(value_item)
                if "description" in data:
                    desc_item = QStandardItem(f"description: {data['description']}")
                    parentItem.appendRow(desc_item)
            else:

                for key, value in data.items():
                    item = QStandardItem(str(key))
                    parentItem.appendRow(item)
                    self._addDataRecursive(value, item)
        elif isinstance(data, list):
            for element in data:
                self._addDataRecursive(element, parentItem)
        else:
            item = QStandardItem(str(data))
            parentItem.appendRow(item)
    
    def showTestData(self):
        test_data = {
            "PersonA": {
                "info": {
                    "age": 42,
                    "email": "a@example.com"
                },
                "hobbies": ["Reading", "Swimming"]
            },
            "PersonB": {
                "info": {
                    "age": 35,
                    "email": "b@example.com",
                    "address": {
                        "street": "Main St",
                        "city": "Berlin"
                    }
                }
            }
        }

        self.showData(test_data)
