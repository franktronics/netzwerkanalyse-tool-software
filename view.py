import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QListWidget
import controller

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Netzwerkanalyse Tool")
        self.setGeometry(100, 100, 600, 400)
        
        bigBox = QVBoxLayout()

        # Start-Button
        self.start_button = QPushButton("Start Sniffer")
        self.start_button.clicked.connect(self.start_sniffing)  
        boxStart = QHBoxLayout()
        boxStart.addWidget(self.start_button)
        bigBox.addLayout(boxStart)

        # Liste zur Anzeige der Pakete
        self.list_widget = QListWidget()
        bigBox.addWidget(self.list_widget)

        # Ende-Button
        self.end_button = QPushButton("Beenden")
        self.end_button.clicked.connect(self.closeEvent)  
        boxEnd = QHBoxLayout()
        boxEnd.addWidget(self.end_button)
        bigBox.addLayout(boxEnd)

        self.setLayout(bigBox)
        self.show()
    
    def start_sniffing(self):
        """Ruft den Sniffer aus dem Controller auf und aktualisiert die Liste."""
        self.list_widget.clear()
        packets = controller.start_sniffer()
        
        for i, (protocol, data) in enumerate(packets):
            display_text = f"{i+1}. {protocol} | Länge: {len(data)} Bytes"
            self.list_widget.addItem(display_text)

    def closeEvent(self, event):
        """Fragt den Nutzer, ob das Programm beendet werden soll."""
        r = QMessageBox.question(self, "Beenden?", "Möchten Sie das Programm wirklich beenden?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
