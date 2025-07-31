
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from services import playlist_manager
from services.spotify_auth import get_spotify_client

class DeletePlaylistPage(QWidget):
    def __init__(self, go_back):
        super().__init__()
        self.setStyleSheet("""
            QWidget { background-color: #212121; color: #b3b3b3; }
            QLabel#titleLabel { color: #1db954; font-size: 28px; font-weight: bold; margin-bottom: 18px; }
            QLineEdit { background-color: #121212; color: #b3b3b3; border: 1px solid #535353; border-radius: 8px; padding: 8px; font-size: 16px; }
            QPushButton { background-color: #1db954; color: #121212; border-radius: 8px; padding: 8px 18px; font-size: 16px; font-weight: 500; }
            QPushButton:hover { background-color: #535353; color: #1db954; }
            QListWidget { background-color: #121212; color: #b3b3b3; border: 1px solid #535353; border-radius: 8px; font-size: 15px; }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(32, 32, 32, 32)

        self.playlist_image_label = QLabel()
        self.playlist_image_label.setAlignment(Qt.AlignCenter)
        self.playlist_image_label.setFixedHeight(120)
        layout.addWidget(self.playlist_image_label)

        self.playlist_name_label = QLabel("")
        self.playlist_name_label.setObjectName("titleLabel")
        self.playlist_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.playlist_name_label)

        self.label = QLabel("Enter Playlist ID:")
        layout.addWidget(self.label)

        self.playlist_input = QLineEdit()
        layout.addWidget(self.playlist_input)

        self.load_button = QPushButton("Load Playlist")
        layout.addWidget(self.load_button)

        self.track_list = QListWidget()
        layout.addWidget(self.track_list)

        btn_row = QHBoxLayout()
        self.remove_button = QPushButton("Remove Selected Tracks")
        btn_row.addWidget(self.remove_button)
        self.back_btn = QPushButton("Return to Menu")
        self.back_btn.clicked.connect(go_back)
        btn_row.addWidget(self.back_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)

        self.tracks_uri_map = {}
        self.load_button.clicked.connect(self.load_tracks)
        self.remove_button.clicked.connect(self.remove_tracks)

    def load_tracks(self):
        self.track_list.clear()
        playlist_id = self.playlist_input.text().strip()

        try:
            sp = get_spotify_client()
            # Get playlist info
            playlist = sp.playlist(playlist_id)
            name = playlist.get('name', '')
            images = playlist.get('images', [])
            self.playlist_name_label.setText(name)
            if images:
                from urllib.request import urlopen
                from PyQt5.QtGui import QPixmap, QImage
                try:
                    img_data = urlopen(images[0]['url']).read()
                    image = QImage()
                    image.loadFromData(img_data)
                    pixmap = QPixmap(image)
                    self.playlist_image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                except Exception:
                    self.playlist_image_label.setText("[Image unavailable]")
            else:
                self.playlist_image_label.setText("[No image]")

            all_tracks = playlist_manager.get_all_tracks(playlist_id)
            self.tracks_uri_map.clear()

            for item in all_tracks:
                track = item['track']
                if not track:
                    continue
                name = track['name']
                artists = ', '.join([a['name'] for a in track['artists']])
                display = f"{name} - {artists}"
                list_item = QListWidgetItem(display)
                list_item.setCheckState(Qt.Unchecked)
                self.track_list.addItem(list_item)
                self.tracks_uri_map[display] = track['uri']
        except Exception as e:
            self.playlist_name_label.setText("")
            self.playlist_image_label.setText("")
            QMessageBox.critical(self, "Error", str(e))

    def remove_tracks(self):
        playlist_id = self.playlist_input.text().strip()
        selected_uris = []

        for i in range(self.track_list.count()):
            item = self.track_list.item(i)
            if item.checkState():
                selected_uris.append(self.tracks_uri_map[item.text()])

        if not selected_uris:
            QMessageBox.information(self, "Info", "No tracks selected.")
            return

        try:
            playlist_manager.remove_tracks(playlist_id, selected_uris)
            QMessageBox.information(self, "Done", "Tracks removed!")
            self.load_tracks()  # Refresh the track list after removal
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
