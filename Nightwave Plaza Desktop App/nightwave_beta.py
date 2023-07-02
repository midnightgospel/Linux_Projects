import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class NightwavePlazaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nightwave Plaza Player")

        # Apply a dark theme to the application
        self.setStyleSheet("background-color: #333333; color: #FFFFFF;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)
        self.song_info_layout = QVBoxLayout()
        self.button_layout = QVBoxLayout()
        self.artwork_layout = QVBoxLayout()

        self.title_label = QLabel(self.central_widget)
        self.album_label = QLabel(self.central_widget)
        self.artist_label = QLabel(self.central_widget)
        self.listener_count_label = QLabel(self.central_widget)
        self.play_button = QPushButton("Play", self.central_widget)
        self.stop_button = QPushButton("Stop", self.central_widget)
        self.artwork_image = QLabel(self.central_widget)

        self.song_info_layout.addWidget(self.title_label)
        self.song_info_layout.addWidget(self.album_label)
        self.song_info_layout.addWidget(self.artist_label)
        self.song_info_layout.addWidget(self.listener_count_label)

        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.stop_button)

        self.artwork_layout.addWidget(self.artwork_image)

        self.layout.addLayout(self.song_info_layout)
        self.layout.addLayout(self.artwork_layout)
        self.layout.addLayout(self.button_layout)

        self.play_button.setFixedSize(60, 30)
        self.stop_button.setFixedSize(60, 30)

        self.play_button.clicked.connect(self.play)
        self.stop_button.clicked.connect(self.stop)

        self.media_player = QMediaPlayer(self)
        self.update_song_info()

        # Autoplay when the script starts
        self.play()

    def update_song_info(self):
        try:
            response = requests.get("https://api.plaza.one/status")
            data = response.json()
            song_info = data.get("song", {})
            title = song_info.get("title", "-")
            album = song_info.get("album", "-")
            artist = song_info.get("artist", "-")
            artwork_src = song_info.get("artwork_src")
            listener_count = data.get("listeners", "-")

            self.title_label.setText(f"Title: {title}")
            self.album_label.setText(f"Album: {album}")
            self.artist_label.setText(f"Artist: {artist}")
            self.listener_count_label.setText(f"Listener Count: {listener_count}")

            if artwork_src:
                response = requests.get(artwork_src)
                image_data = response.content

                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                scaled_pixmap = pixmap.transformed(QTransform().scale(0.5, 0.5), Qt.SmoothTransformation)
                self.artwork_image.setPixmap(scaled_pixmap)
                self.artwork_image.setScaledContents(True)  # Scale the pixmap to fit the label
            else:
                self.artwork_image.clear()

        except Exception as e:
            print(f"Error: {str(e)}")

        # Schedule the next update
        QTimer.singleShot(1000, self.update_song_info)

    def play(self):
        self.media_player.setMedia(QMediaContent(QUrl("https://plaza.one/mp3")))
        self.media_player.play()

    def stop(self):
        self.media_player.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = NightwavePlazaPlayer()
    player.setGeometry(100, 100, 600, 200)  # Adjust window size and position
    player.show()
    sys.exit(app.exec_())
