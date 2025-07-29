from gui.main_window import MainWindow
from gui.auth_page import AuthPage
from PyQt5.QtWidgets import QApplication, QStackedWidget
import sys
import os

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    stack = QStackedWidget()
    stack.setFixedSize(1280, 720)

    def on_auth(client_id, client_secret):
        os.environ["SPOTIPY_CLIENT_ID"] = client_id
        os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
        stack.removeWidget(auth_page)
        main_window = MainWindow()
        stack.addWidget(main_window)
        stack.setCurrentWidget(main_window)

    auth_page = AuthPage(on_auth)
    stack.addWidget(auth_page)
    stack.setCurrentWidget(auth_page)
    stack.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
