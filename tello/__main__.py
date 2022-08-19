from gui.tellogui import TelloGui 
from PyQt6.QtWidgets import QApplication
from sys import argv, exit

if __name__ == '__main__':
    app = QApplication(argv)
    TelloGui()
    exit(app.exec())