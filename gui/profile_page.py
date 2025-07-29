
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from services import playlist_manager

class ProfilePage(QWidget):
    def __init__(self, go_back):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(48, 48, 48, 48)
        self.setStyleSheet("""
            QWidget { background-color: #212121; color: #b3b3b3; font-family: 'Segoe UI', Arial, sans-serif; }
            QLabel#titleLabel { color: #1db954; font-size: 36px; font-weight: bold; margin-bottom: 18px; }
            QLabel#infoLabel { background: #181818; border-radius: 12px; padding: 18px; font-size: 18px; color: #b3b3b3; margin-bottom: 12px; }
            QLabel#imageLabel { background: #181818; border-radius: 64px; margin-bottom: 18px; }
            QPushButton { background-color: #1db954; color: #121212; border-radius: 8px; padding: 10px 24px; font-size: 16px; font-weight: 500; }
            QPushButton:hover { background-color: #535353; color: #1db954; }
        """)

        title = QLabel("Profile Page")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.image_label = QLabel()
        self.image_label.setObjectName("imageLabel")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.info_label = QLabel("Loading user info...")
        self.info_label.setObjectName("infoLabel")
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)

        self.playlists_label = QLabel("Your Playlists:")
        self.playlists_label.setStyleSheet("font-size: 20px; color: #1db954; font-weight: bold; margin-top: 18px;")
        layout.addWidget(self.playlists_label)

        from PyQt5.QtWidgets import QScrollArea, QWidget, QGridLayout
        self.playlists_area = QScrollArea()
        self.playlists_area.setWidgetResizable(True)
        self.playlists_widget = QWidget()
        self.playlists_layout = QGridLayout()
        self.playlists_layout.setSpacing(16)
        self.playlists_widget.setLayout(self.playlists_layout)
        self.playlists_area.setWidget(self.playlists_widget)
        layout.addWidget(self.playlists_area)

        back_btn = QPushButton("Return to Menu")
        back_btn.clicked.connect(go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)
        self.load_user_info()

    def load_user_info(self):
        try:
            from services.spotify_auth import get_spotify_client
            sp = get_spotify_client()
            user = sp.current_user()
            name = user.get('display_name', 'Unknown')
            email = user.get('email', 'Unknown')
            followers = user.get('followers', {}).get('total', 0)
            info = f"<b>Name:</b> {name}<br>"
            info += f"<b>Email:</b> {email}<br>"
            info += f"<b>Followers:</b> {followers}<br>"
            self.info_label.setText(info)

            images = user.get('images', [])
            if images:
                from urllib.request import urlopen
                from PyQt5.QtGui import QImage
                try:
                    img_data = urlopen(images[0]['url']).read()
                    image = QImage()
                    image.loadFromData(img_data)
                    pixmap = QPixmap(image)
                    self.image_label.setPixmap(pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                except Exception:
                    self.image_label.setText("[Profile image unavailable]")
            else:
                self.image_label.setText("[No profile image]")

            # Load all user playlists
            playlists = []
            results = sp.current_user_playlists()
            while results:
                playlists.extend(results['items'])
                results = sp.next(results) if results.get('next') else None

            # Clear previous widgets
            for i in reversed(range(self.playlists_layout.count())):
                widget = self.playlists_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            from PyQt5.QtWidgets import QLabel
            from PyQt5.QtGui import QPixmap, QImage
            from urllib.request import urlopen
            for idx, playlist in enumerate(playlists):
                pl_name = playlist.get('name', '')
                pl_img_label = QLabel()
                pl_img_label.setAlignment(Qt.AlignCenter)
                pl_img_label.setFixedSize(80, 80)
                pl_images = playlist.get('images', [])
                if pl_images:
                    try:
                        img_data = urlopen(pl_images[0]['url']).read()
                        image = QImage()
                        image.loadFromData(img_data)
                        pixmap = QPixmap(image)
                        pl_img_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    except Exception:
                        pl_img_label.setText("[Image]")
                else:
                    pl_img_label.setText("[No image]")
                pl_name_label = QLabel(pl_name)
                pl_name_label.setAlignment(Qt.AlignCenter)
                pl_name_label.setStyleSheet("font-size: 15px; color: #b3b3b3; margin-bottom: 8px;")
                self.playlists_layout.addWidget(pl_img_label, idx, 0)
                self.playlists_layout.addWidget(pl_name_label, idx, 1)
        except Exception as e:
            self.info_label.setText(f"Error loading user info: {e}")
