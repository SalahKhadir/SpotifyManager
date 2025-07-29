from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class AuthPage(QWidget):
    def __init__(self, on_auth):
        super().__init__()
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #b3b3b3; font-family: 'Segoe UI', Arial, sans-serif; }
            QLabel#titleLabel { color: #1db954; font-size: 32px; font-weight: bold; margin-bottom: 18px; }
            QLineEdit { background-color: #181818; color: #b3b3b3; border: 1px solid #535353; border-radius: 8px; padding: 8px; font-size: 16px; }
            QPushButton { background-color: #1db954; color: #121212; border-radius: 8px; padding: 10px 24px; font-size: 16px; font-weight: 500; }
            QPushButton:hover { background-color: #535353; color: #1db954; }
        """)
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Spotify Authentication")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("SPOTIPY_CLIENT_ID")
        layout.addWidget(self.client_id_input)

        self.client_secret_input = QLineEdit()
        self.client_secret_input.setPlaceholderText("SPOTIPY_CLIENT_SECRET")
        self.client_secret_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.client_secret_input)

        self.login_btn = QPushButton("Login")
        layout.addWidget(self.login_btn)

        self.setLayout(layout)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(pal)
        self.login_btn.clicked.connect(self.authenticate)
        self.on_auth = on_auth

    def authenticate(self):
        import os
        client_id = self.client_id_input.text().strip()
        client_secret = self.client_secret_input.text().strip()
        if not client_id or not client_secret:
            QMessageBox.warning(self, "Missing Info", "Please enter both Client ID and Client Secret.")
            return
        os.environ['SPOTIPY_CLIENT_ID'] = client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
        # Set redirect URI from .env or use default
        redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')
        os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri
        self.on_auth(client_id, client_secret)
