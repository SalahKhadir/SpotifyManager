# main.py
from PyQt5.QtWidgets import QApplication, QStackedWidget
from gui.auth_page import AuthPage
from gui.main_window import MainWindow
import sys

class App(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Toolkit")
        self.setGeometry(200, 100, 900, 980)

        self.auth_page = AuthPage(self.goto_home)
        self.home_page = MainWindow(self.goto_auth)

        self.addWidget(self.auth_page)
        self.addWidget(self.home_page)

        self.setCurrentWidget(self.auth_page)

    def goto_home(self):
        self.setCurrentWidget(self.home_page)

    def goto_auth(self):
        self.setCurrentWidget(self.auth_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
