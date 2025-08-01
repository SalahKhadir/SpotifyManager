
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout, QGridLayout, QScrollArea, QSizePolicy
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

        self.go_back = go_back
        self.tracks_uri_map = {}
        self.playlists = []
        self.selected_playlist = None

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(18)
        self.main_layout.setContentsMargins(32, 32, 32, 32)
        self.setLayout(self.main_layout)

        self.playlist_grid_widget = QWidget()
        self.playlist_grid_layout = QGridLayout()
        self.playlist_grid_layout.setSpacing(24)
        self.playlist_grid_widget.setLayout(self.playlist_grid_layout)


        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.playlist_grid_widget)
        self.main_layout.addWidget(self.scroll)

        # Add Return to Menu button under the grid
        self.menu_btn_row = QHBoxLayout()
        self.menu_btn_row.addStretch()
        self.return_menu_btn = QPushButton("Return to Menu")
        self.return_menu_btn.setStyleSheet("background-color: #1db954; color: #121212; border-radius: 8px; padding: 10px 24px; font-size: 16px; font-weight: 500;")
        self.return_menu_btn.clicked.connect(self.go_back)
        self.menu_btn_row.addWidget(self.return_menu_btn)
        self.menu_btn_row.addStretch()
        self.main_layout.addLayout(self.menu_btn_row)

        self.tracks_widget = QWidget()
        self.tracks_layout = QVBoxLayout()
        self.tracks_widget.setLayout(self.tracks_layout)
        self.tracks_widget.hide()
        self.main_layout.addWidget(self.tracks_widget)

        # Playlist info in tracks view
        self.playlist_image_label = QLabel()
        self.playlist_image_label.setAlignment(Qt.AlignCenter)
        self.playlist_image_label.setFixedHeight(120)
        self.tracks_layout.addWidget(self.playlist_image_label)

        self.playlist_name_label = QLabel("")
        self.playlist_name_label.setObjectName("titleLabel")
        self.playlist_name_label.setAlignment(Qt.AlignCenter)
        self.tracks_layout.addWidget(self.playlist_name_label)

        self.track_list = QListWidget()
        self.tracks_layout.addWidget(self.track_list)

        btn_row = QHBoxLayout()
        self.remove_button = QPushButton("Remove Selected Tracks")
        btn_row.addWidget(self.remove_button)
        self.back_btn = QPushButton("Back to Playlists")
        self.back_btn.clicked.connect(self.show_playlists)
        btn_row.addWidget(self.back_btn)
        self.tracks_layout.addLayout(btn_row)

        self.remove_button.clicked.connect(self.remove_tracks)
        self.load_playlists()

    def show_playlists(self):
        self.tracks_widget.hide()
        self.scroll.show()

    def show_tracks(self, playlist):
        self.selected_playlist = playlist
        self.scroll.hide()
        self.tracks_widget.show()
        self.load_tracks(playlist['id'])
    def load_playlists(self):
        try:
            sp = get_spotify_client()
            user_id = sp.current_user()['id']
            playlists = []
            results = sp.current_user_playlists()
            playlists.extend(results['items'])
            while results['next']:
                results = sp.next(results)
                playlists.extend(results['items'])
            # Only show playlists owned by the current user
            owned_playlists = [pl for pl in playlists if pl.get('owner', {}).get('id') == user_id]
            self.playlists = owned_playlists
            # Clear grid
            for i in reversed(range(self.playlist_grid_layout.count())):
                widget = self.playlist_grid_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            # Add playlist cards
            for idx, pl in enumerate(owned_playlists):
                card = self.create_playlist_card(pl)
                row, col = divmod(idx, 3)
                self.playlist_grid_layout.addWidget(card, row, col)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load playlists: {e}")

    def create_playlist_card(self, playlist):
        card = QPushButton()
        card.setStyleSheet("""
            QPushButton {
                background-color: #181818;
                color: #b3b3b3;
                border-radius: 18px;
                border: 2px solid #535353;
                font-size: 18px;
                font-weight: 600;
                padding: 16px;
                min-width: 220px;
                min-height: 220px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #1db954;
                color: #121212;
                border: 2px solid #1db954;
            }
        """)
        vbox = QVBoxLayout(card)
        vbox.setAlignment(Qt.AlignCenter)
        img_label = QLabel()
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setFixedSize(120, 120)
        if playlist.get('images'):
            from urllib.request import urlopen
            from PyQt5.QtGui import QPixmap, QImage
            try:
                img_data = urlopen(playlist['images'][0]['url']).read()
                image = QImage()
                image.loadFromData(img_data)
                pixmap = QPixmap(image)
                img_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except Exception:
                img_label.setText("[Image unavailable]")
        else:
            img_label.setText("[No image]")
        vbox.addWidget(img_label)
        name_label = QLabel(playlist.get('name', ''))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 20px; color: #1db954; font-weight: bold;")
        vbox.addWidget(name_label)
        card.clicked.connect(lambda: self.show_tracks(playlist))
        return card

    # No longer needed

    def load_tracks(self, playlist_id):
        self.track_list.clear()
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
        if not self.selected_playlist:
            return
        playlist_id = self.selected_playlist['id']
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
            self.load_tracks(playlist_id)  # Refresh the track list after removal
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
