# gui/auth_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from dotenv import set_key, load_dotenv
import os

class AuthPage(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setStyleSheet("background-color: #121212; color: #b3b3b3; font-size: 16px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(60, 80, 60, 80)
        layout.setSpacing(20)

        title = QLabel("Spotify Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1db954; font-size: 32px; font-weight: bold;")
        layout.addWidget(title)

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("SPOTIPY_CLIENT_ID")
        self.client_id_input.setStyleSheet("background-color: #212121; padding: 8px; color: white; border-radius: 8px;")
        layout.addWidget(self.client_id_input)

        self.client_secret_input = QLineEdit()
        self.client_secret_input.setPlaceholderText("SPOTIPY_CLIENT_SECRET")
        self.client_secret_input.setEchoMode(QLineEdit.Password)
        self.client_secret_input.setStyleSheet("background-color: #212121; padding: 8px; color: white; border-radius: 8px;")
        layout.addWidget(self.client_secret_input)

        login_btn = QPushButton("Login to Spotify")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #1db954;
                color: black;
                font-size: 18px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1ed760;
            }
        """)
        login_btn.clicked.connect(self.save_and_login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def save_and_login(self):
        client_id = self.client_id_input.text().strip()
        client_secret = self.client_secret_input.text().strip()

        if not client_id or not client_secret:
            QMessageBox.warning(self, "Error", "Please enter both Client ID and Secret")
            return

        # Clear token cache for this account
        if os.path.exists(f".cache-{client_id}"):
            os.remove(f".cache-{client_id}")

        # Save to .env file
        set_key(".env", "SPOTIPY_CLIENT_ID", client_id)
        set_key(".env", "SPOTIPY_CLIENT_SECRET", client_secret)
        set_key(".env", "SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

        # Update in-memory environment variables
        os.environ["SPOTIPY_CLIENT_ID"] = client_id
        os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
        os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:8888/callback"

        # Reload env so spotify_auth will see it
        load_dotenv(override=True)

        try:
            # Import AFTER setting env vars so it picks up correct values
            from services.spotify_auth import get_spotify_client
            sp = get_spotify_client()
            _ = sp.current_user()

            QMessageBox.information(self, "Success", "Spotify authentication successful!")
            self.on_success()

        except Exception as e:
            QMessageBox.critical(self, "Auth Failed", str(e))
