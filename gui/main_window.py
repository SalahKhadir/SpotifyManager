from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .new_playlist import NewPlaylistPage
from .sort_playlist import SortPlaylistPage
from .delete_playlist import DeletePlaylistPage
from .profile_page import ProfilePage
from services.spotify_auth import get_spotify_client
import requests
import os
import glob

class MainWindow(QMainWindow):
    def __init__(self, go_back):
        super().__init__()
        self.go_back = go_back
        self.setStyleSheet("background-color: #121212;")
        self.setGeometry(100, 100, 850, 980)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_widget = self.create_home()
        self.new_playlist = NewPlaylistPage(self.return_home)
        self.sort_playlist = SortPlaylistPage(self.return_home)
        self.delete_playlist = DeletePlaylistPage(self.return_home)
        self.profile_page = ProfilePage(self.return_home)

        self.stack.addWidget(self.home_widget)
        self.stack.addWidget(self.new_playlist)
        self.stack.addWidget(self.sort_playlist)
        self.stack.addWidget(self.delete_playlist)
        self.stack.addWidget(self.profile_page)

        # Always try to load user profile when showing home
        self.load_user_profile()

    def load_user_profile(self):
        try:
            sp = get_spotify_client()
            profile = sp.current_user()
            if not profile or 'display_name' not in profile:
                self.username_label.setText("Unknown User")
                self.profile_pic.clear()
                return
            self.username_label.setText(profile['display_name'] or "Unknown User")

            # Load profile image
            if profile.get('images'):
                img_url = profile['images'][0]['url']
                img_data = requests.get(img_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                self.profile_pic.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.profile_pic.clear()
        except Exception:
            self.username_label.setText("Unknown User")
            self.profile_pic.clear()

    def return_home(self):
        self.stack.setCurrentWidget(self.home_widget)
        self.load_user_profile()

    def create_home(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(32)

        # Top bar layout to add logout button on the top right
        top_bar = QHBoxLayout()
        top_bar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        logout_btn = QPushButton("Logout")
        logout_btn.setFixedSize(120, 40)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #b3b3b3;
                color: #121212;
                font-weight: bold;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1db954;
                color: white;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        top_bar.addWidget(logout_btn)

        layout.addLayout(top_bar)

        title = QLabel("Spotify Toolkit")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1db954; font-size: 40px; font-weight: bold;")
        layout.addWidget(title)

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row1.setSpacing(32)
        row2.setSpacing(32)

        buttons = [
            ("New Playlist", lambda: self.stack.setCurrentWidget(self.new_playlist)),
            ("Sort Playlist", lambda: self.stack.setCurrentWidget(self.sort_playlist)),
            ("Delete from Playlist", lambda: self.stack.setCurrentWidget(self.delete_playlist)),
            ("Profile", lambda: self.stack.setCurrentWidget(self.profile_page)),
        ]

        for i, (label, action) in enumerate(buttons):
            btn = QPushButton(label)
            btn.clicked.connect(action)
            btn.setFixedSize(350, 180)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1db954;
                    color: #121212;
                    font-size: 24px;
                    font-weight: 600;
                    border-radius: 18px;
                }
                QPushButton:hover {
                    background-color: #212121;
                    color: #1db954;
                    border: 2px solid #1db954;
                }
            """)
            (row1 if i < 2 else row2).addWidget(btn)

        layout.addLayout(row1)
        layout.addLayout(row2)

        # Bottom bar for profile info
        bottom_bar = QHBoxLayout()
        self.username_label = QLabel("Loading...")
        self.username_label.setStyleSheet("color: white; font-size: 16px;")
        bottom_bar.addWidget(self.username_label, alignment=Qt.AlignLeft)

        bottom_bar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.profile_pic = QLabel()
        bottom_bar.addWidget(self.profile_pic, alignment=Qt.AlignRight)

        layout.addStretch()
        layout.addLayout(bottom_bar)

        widget.setLayout(layout)
        return widget

    def logout(self):
        # Delete all Spotify token cache files to log out properly
        for cache_file in glob.glob(".cache-*"):
            try:
                os.remove(cache_file)
            except Exception:
                pass
        if os.path.exists(".cache"):
            try:
                os.remove(".cache")
            except Exception:
                pass

        print("✅ Logged out and cleared cache.")
        self.username_label.setText("Unknown User")
        self.profile_pic.clear()
        self.go_back()  # call the go_back callback to return to AuthPage
