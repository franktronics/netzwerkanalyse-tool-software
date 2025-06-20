from PyQt6.QtWidgets import QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt

class RawDataTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["", "ID", "Timestamp", "NIC", "Packets"])
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setColumnWidth(0, 60)
        for i in range(1, 4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        self._selected_row = -1

    def add_row(self, item: tuple[int, str, str]):
        # item is a tuple with (id, timestamp, nic)
        # Add a new row to the table with the provided data if the id is not already present
        # else update the existing row
        row_count = self.rowCount()
        for row in range(row_count):
            if self.item(row, 1) and self.item(row, 1).text() == str(item[0]):
                # Update only the packets count if the ID already exists
                actual_packets = int(self.item(row, 4).text()) if self.item(row, 4) else 0
                self.setItem(row, 4, QTableWidgetItem(str(actual_packets + 1)))
                return
        # If the ID does not exist, add a new row
        self._insert_row(item)

    def _insert_row(self, item: tuple[int, str, str]):
        # Insert a new row with the provided data
        row_count = self.rowCount()
        self.insertRow(row_count)

        # Create checkbox for selection
        checkbox = QCheckBox()
        checkbox.stateChanged.connect(lambda state, r=row_count: self._on_checkbox_changed(state, r))
        self.setCellWidget(row_count, 0, checkbox)

        # Other columns
        self.setItem(row_count, 1, QTableWidgetItem(str(item[0])))
        self.setItem(row_count, 2, QTableWidgetItem(item[1]))
        self.setItem(row_count, 3, QTableWidgetItem(item[2]))
        self.setItem(row_count, 4, QTableWidgetItem("1"))

    def _on_checkbox_changed(self, state, row: int):
        if state == Qt.CheckState.Checked.value:
            # Uncheck all other checkboxes
            for i in range(self.rowCount()):
                if i != row:
                    checkbox: QCheckBox = QCheckBox(self.cellWidget(i, 0))
                    if checkbox:
                        checkbox.blockSignals(True)  # Prevent recursive calls
                        checkbox.setChecked(False)
                        checkbox.blockSignals(False)
            self.selected_row = row
        else:
            if self.selected_row == row:
                self.selected_row = -1