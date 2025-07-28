import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow  # adjust if your class name or file name is different

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # this sets up all widgets and layouts from ui.py

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
