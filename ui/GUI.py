import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QListWidget

Teilnehmer = [["MacAdresse1", "IP-Adresse1", "Subnetz1"],
              ["MacAdresse2", "IP-Adresse2", "Subnetz2"],
              ["MacAdresse3", "IP-Adresse3", "Subnetz3"],
              ["MacAdresse4", "IP-Adresse4", "Subnetz4"]]

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Netzwerkanalyse Tool")
        bigBox = QVBoxLayout()

        # Start-Button
        self.start_button = QPushButton("&Start")
        self.start_button.clicked.connect(self.start)  # Signal mit Methode verbinden
        boxStart = QHBoxLayout()
        boxStart.addWidget(self.start_button)
        bigBox.addLayout(boxStart)

        # Liste zur Anzeige der Werte
        self.list_widget = QListWidget()
        bigBox.addWidget(self.list_widget)

        # Ende-Button
        self.end_button = QPushButton("&Ende")
        self.end_button.clicked.connect(self.closeEvent)  # Signal mit Methode verbinden
        boxEnd = QHBoxLayout()
        boxEnd.addWidget(self.end_button)
        bigBox.addLayout(boxEnd)

        self.setLayout(bigBox)
        self.show()
    
    def start(self):
        self.list_widget.clear()
        sample_list = [f"{mac}, {ip}, {subnet}" for mac, ip, subnet in Teilnehmer]
        self.list_widget.addItems(sample_list)
    
    def closeEvent(self, ev):
        r = QMessageBox.question(self, "Abfrage", "Beenden?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.Yes:
            ev.accept()
        else:
            ev.ignore()
    
app = QApplication(sys.argv)
w = MyWidget()
app.exec()
