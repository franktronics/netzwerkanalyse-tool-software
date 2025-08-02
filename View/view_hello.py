from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox, QToolBar, QMainWindow, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class ViewHello(QWidget):
    
    #Constructor for centerApplication viewTerminal
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # Titel
        title = QLabel("Willkommen zum Netzwerkanalyse-Tool", self)
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2E4053;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Beschreibung
        lab_description = QLabel(
            "Dieses Tool hilft Ihnen dabei, Netzwerkdaten zu analysieren, "
            "Topologien zu visualisieren und Leistungsmetriken zu erfassen.", self)
        lab_description.setWordWrap(True)
        lab_description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Button
        self.btn_start = QPushButton("Analyse starten", self)
        self.btn_start.setFont(QFont("Arial", 12))
        self.btn_start.setStyleSheet("padding: 10px; background-color: #3498DB; color: white;")
        self.btn_start.setStatusTip("Starte Netzwerkanalyse")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(lab_description)
        layout.addSpacing(30)
        layout.addWidget(self.btn_start)
        layout.setAlignment(self.btn_start, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)