from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from .new_playlist import NewPlaylistPage
from .sort_playlist import SortPlaylistPage
from .delete_playlist import DeletePlaylistPage
from .profile_page import ProfilePage

class MainWindow(QMainWindow):
    def __init__(self, stack=None):
        super().__init__()
        self.setWindowTitle("Spotify Toolkit")
        self.setGeometry(100, 100, 850, 980)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
        """)

        self.stack = stack if stack is not None else QStackedWidget()
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

    def return_home(self):
        self.stack.setCurrentWidget(self.home_widget)

    def create_home(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(32)
        layout.setContentsMargins(40, 40, 40, 40)

        # Top title
        title = QLabel("Spotify Toolkit made by @salah")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #1db954;
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 32px;
        """)
        layout.addWidget(title)

        # Main buttons
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
                    border: 2px solid #1db954;
                    margin: 8px;
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

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("background-color: #535353; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 24px; margin-top: 24px;")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn, alignment=Qt.AlignRight)

        # Profile info at bottom right
        bottom_row = QHBoxLayout()
        bottom_row.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.profile_pic_label = QLabel()
        self.profile_pic_label.setFixedSize(64, 64)
        self.profile_pic_label.setStyleSheet("border-radius: 32px; background: #181818;")
        self.profile_name_label = QLabel("")
        self.profile_name_label.setStyleSheet("color: #b3b3b3; font-size: 18px; font-weight: bold; margin-left: 12px;")
        bottom_row.addWidget(self.profile_name_label)
        bottom_row.addWidget(self.profile_pic_label)
        layout.addLayout(bottom_row)

        widget.setLayout(layout)
        widget.setStyleSheet("background-color: #121212;")

        # Load profile info
        self.load_profile_info()
        return widget

    def logout(self):
        # Remove credentials and go back to AuthPage
        import os
        os.environ.pop("SPOTIPY_CLIENT_ID", None)
        os.environ.pop("SPOTIPY_CLIENT_SECRET", None)
        from gui.auth_page import AuthPage
        auth_page = AuthPage(self.stack.parent().on_auth if hasattr(self.stack.parent(), 'on_auth') else lambda cid, cs: None)
        self.stack.addWidget(auth_page)
        self.stack.setCurrentWidget(auth_page)

    def load_profile_info(self):
        try:
            from services import playlist_manager
            user = playlist_manager.sp.current_user()
            name = user.get('display_name', '')
            self.profile_name_label.setText(name)
            images = user.get('images', [])
            if images:
                from urllib.request import urlopen
                from PyQt5.QtGui import QPixmap, QImage
                try:
                    img_data = urlopen(images[0]['url']).read()
                    image = QImage()
                    image.loadFromData(img_data)
                    pixmap = QPixmap(image)
                    self.profile_pic_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                except Exception:
                    self.profile_pic_label.setText("")
            else:
                self.profile_pic_label.setText("")
        except Exception:
            self.profile_name_label.setText("")
            self.profile_pic_label.setText("")
