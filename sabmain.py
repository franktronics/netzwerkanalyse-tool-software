import sys
from PySide6.QtWidgets import QApplication
import view

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = view.MyWidget()
    app.exec()
