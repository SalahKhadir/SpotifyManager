
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout, QComboBox, QGridLayout, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt
from services import playlist_manager
from services.spotify_auth import get_spotify_client
from services.spotify_auth import get_spotify_client

class SortPlaylistPage(QWidget):
    def sort_tracks(self):
        # Sort the track_meta list based on the selected sort option
        sort_option = self.sort_combo.currentText()
        if not self.track_meta:
            return
        if sort_option == "Alphabetic (A-Z)":
            sorted_tracks = sorted(self.track_meta, key=lambda x: x['name'].lower())
        elif sort_option == "Alphabetic (Z-A)":
            sorted_tracks = sorted(self.track_meta, key=lambda x: x['name'].lower(), reverse=True)
        elif sort_option == "Date Added (Oldest First)":
            sorted_tracks = sorted(self.track_meta, key=lambda x: x['date_added'])
        elif sort_option == "Date Added (Newest First)":
            sorted_tracks = sorted(self.track_meta, key=lambda x: x['date_added'], reverse=True)
        elif sort_option == "Release Date (Oldest First)":
            sorted_tracks = sorted(self.track_meta, key=lambda x: x['release_date'])
        elif sort_option == "Release Date (Newest First)":
            sorted_tracks = sorted(self.track_meta, key=lambda x: x['release_date'], reverse=True)
        else:
            sorted_tracks = self.track_meta
        # Update the QListWidget with the sorted order
        self.track_list.clear()
        for track in sorted_tracks:
            list_item = QListWidgetItem(track['display'])
            self.track_list.addItem(list_item)
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
        self.uris_in_order = []
        self.track_meta = []
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
        self.tracks_layout.addLayout(sort_row)

        self.track_list = QListWidget()
        self.track_list.setDragDropMode(QListWidget.InternalMove)
        self.tracks_layout.addWidget(self.track_list)

        btn_row = QHBoxLayout()
        self.save_button = QPushButton("Save New Order")
        btn_row.addWidget(self.save_button)
        self.back_btn = QPushButton("Back to Playlists")
        self.back_btn.clicked.connect(self.show_playlists)
        btn_row.addWidget(self.back_btn)
        self.tracks_layout.addLayout(btn_row)

        self.save_button.clicked.connect(self.save_order)
        self.sort_button.clicked.connect(self.sort_tracks)
        self.load_playlists()

    def save_order(self):
        playlist_id = None
        if self.selected_playlist:
            playlist_id = self.selected_playlist.get('id')
        if not playlist_id:
            QMessageBox.warning(self, "No Playlist", "No playlist selected.")
            return
        try:
            # Get the new order from the QListWidget
            new_uris = []
            for i in range(self.track_list.count()):
                display = self.track_list.item(i).text()
                uri = self.tracks_uri_map.get(display)
                if uri:
                    new_uris.append(uri)
            # Remove all tracks and add them back in the new order (API limit: 100 per call)
            playlist_manager.remove_tracks(playlist_id, self.uris_in_order)
            for i in range(0, len(new_uris), 100):
                playlist_manager.add_tracks_to_playlist(playlist_id, new_uris[i:i+100])
            QMessageBox.information(self, "Done", "Playlist order updated!")
            self.load_tracks(playlist_id)  # Refresh
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

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

    def load_tracks(self, playlist_id):
        self.track_list.clear()
        try:
            all_tracks = playlist_manager.get_all_tracks(playlist_id)
        except Exception as e:
            self.playlist_name_label.setText("")
            self.playlist_image_label.setText("")
            QMessageBox.critical(self, "Error", str(e))
            return

        self.tracks_uri_map.clear()
        self.uris_in_order = []
        self.track_meta = []

        sp = get_spotify_client()
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
