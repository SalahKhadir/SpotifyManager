from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class NewPlaylistPage(QWidget):
    def __init__(self, go_back):
        super().__init__()
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #212121; color: #b3b3b3;")
        
        label = QLabel("🎶 Create a New Playlist Page 🎶")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 22px;")
        
        back_btn = QPushButton("Return to Menu")
        back_btn.clicked.connect(go_back)
        back_btn.setStyleSheet("background-color: #535353; color: white;")

        layout.addWidget(label)
        layout.addWidget(back_btn)
        self.setLayout(layout)
