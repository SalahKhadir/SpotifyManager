
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from services import playlist_manager
from services.spotify_auth import get_spotify_client

class SortPlaylistPage(QWidget):
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

        sort_row = QHBoxLayout()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Alphabetic (A-Z)",
            "Alphabetic (Z-A)",
            "Date Added (Oldest First)",
            "Date Added (Newest First)",
            "Release Date (Oldest First)",
            "Release Date (Newest First)"
        ])
        sort_row.addWidget(QLabel("Sort by:"))
        sort_row.addWidget(self.sort_combo)
        self.sort_button = QPushButton("Sort")
        sort_row.addWidget(self.sort_button)
        layout.addLayout(sort_row)

        self.track_list = QListWidget()
        self.track_list.setDragDropMode(QListWidget.InternalMove)
        layout.addWidget(self.track_list)

        btn_row = QHBoxLayout()
        self.save_button = QPushButton("Save New Order")
        btn_row.addWidget(self.save_button)
        self.back_btn = QPushButton("Return to Menu")
        self.back_btn.clicked.connect(go_back)
        btn_row.addWidget(self.back_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)

        self.tracks_uri_map = {}
        self.uris_in_order = []
        self.track_meta = []  # Store meta info for sorting
        self.load_button.clicked.connect(self.load_tracks)
        self.save_button.clicked.connect(self.save_order)
        self.sort_button.clicked.connect(self.sort_tracks)

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
            self.uris_in_order = []
            self.track_meta = []

            for item in all_tracks:
                track = item['track']
                if not track:
                    continue
                name = track['name']
                artists = ', '.join([a['name'] for a in track['artists']])
                display = f"{name} - {artists}"
                list_item = QListWidgetItem(display)
                self.track_list.addItem(list_item)
                self.tracks_uri_map[display] = track['uri']
                self.uris_in_order.append(track['uri'])
                # Store meta info for sorting
                release_date = track.get('album', {}).get('release_date', '')
                self.track_meta.append({
                    'display': display,
                    'uri': track['uri'],
                    'name': name,
                    'artists': artists,
                    'date_added': item.get('added_at', ''),
                    'release_date': release_date
                })
        except Exception as e:
            self.playlist_name_label.setText("")
            self.playlist_image_label.setText("")
            QMessageBox.critical(self, "Error", str(e))
    def sort_tracks(self):
        option = self.sort_combo.currentText()
        if not self.track_meta:
            return
        tracks = self.track_meta.copy()
        if option == "Alphabetic (A-Z)":
            tracks.sort(key=lambda x: x['name'].lower())
        elif option == "Alphabetic (Z-A)":
            tracks.sort(key=lambda x: x['name'].lower(), reverse=True)
        elif option == "Date Added (Oldest First)":
            tracks.sort(key=lambda x: x['date_added'] or '', reverse=False)
        elif option == "Date Added (Newest First)":
            tracks.sort(key=lambda x: x['date_added'] or '', reverse=True)
        elif option == "Release Date (Oldest First)":
            tracks.sort(key=lambda x: x['release_date'] or '', reverse=False)
        elif option == "Release Date (Newest First)":
            tracks.sort(key=lambda x: x['release_date'] or '', reverse=True)
        self.track_list.clear()
        self.uris_in_order = []
        for meta in tracks:
            list_item = QListWidgetItem(meta['display'])
            self.track_list.addItem(list_item)
            self.tracks_uri_map[meta['display']] = meta['uri']
            self.uris_in_order.append(meta['uri'])

    def save_order(self):
        playlist_id = self.playlist_input.text().strip()
        new_uris = []
        for i in range(self.track_list.count()):
            item = self.track_list.item(i)
            new_uris.append(self.tracks_uri_map[item.text()])

        if not new_uris:
            QMessageBox.information(self, "Info", "No tracks to save.")
            return

        try:
            # Remove all tracks and add them back in the new order (API limit: 100 per call)
            playlist_manager.remove_tracks(playlist_id, self.uris_in_order)
            for i in range(0, len(new_uris), 100):
                playlist_manager.add_tracks_to_playlist(playlist_id, new_uris[i:i+100])
            QMessageBox.information(self, "Done", "Playlist order updated!")
            self.load_tracks()  # Refresh
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
