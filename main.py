import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QSlider, QLabel, \
    QHBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QSizePolicy


class ControlWindow(QWidget):
    def __init__(self, player):
        super().__init__()
        self.player = player

        self.setWindowTitle("Control Panel")
        self.setGeometry(850, 100, 200, 400)

        # Create Play button
        playButton = QPushButton('Play')
        playButton.clicked.connect(self.player.play_video)

        # Create Pause button
        pauseButton = QPushButton('Pause')
        pauseButton.clicked.connect(self.player.pause_video)

        # Create Open button
        openButton = QPushButton('Open')
        openButton.clicked.connect(self.player.open_file)

        # Create buttons for different playback speeds
        play2xButton = QPushButton('Play 2x')
        play2xButton.clicked.connect(self.player.play_2x)

        play5xButton = QPushButton('Play 5x')
        play5xButton.clicked.connect(self.player.play_5x)

        play10xButton = QPushButton('Play 10x')
        play10xButton.clicked.connect(self.player.play_10x)

        playSlowButton = QPushButton('Play Slow (0.5x)')
        playSlowButton.clicked.connect(self.player.play_slow)

        # Create a QLabel to display the time code when paused
        self.timeCodeLabel = QLabel("Time Code: 0:00")

        # Create a layout for the buttons
        layout = QVBoxLayout()
        layout.addWidget(playButton)
        layout.addWidget(pauseButton)
        layout.addWidget(self.timeCodeLabel)  # Add the time code label below the pause button
        layout.addWidget(openButton)
        layout.addWidget(play2xButton)
        layout.addWidget(play5xButton)
        layout.addWidget(play10xButton)
        layout.addWidget(playSlowButton)

        self.setLayout(layout)


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Video Player")
        self.setGeometry(100, 100, 800, 450)  # Adjust the window size

        # Create a QMediaPlayer object
        self.mediaPlayer = QMediaPlayer()

        # Create a QVideoWidget object
        videoWidget = QVideoWidget()

        # Create a QSlider for the timeline
        self.timeline = QSlider(Qt.Orientation.Horizontal)
        self.timeline.setRange(0, 0)
        self.timeline.sliderMoved.connect(self.set_position)

        # Create a QLabel for displaying the current time and total duration
        self.currentTimeLabel = QLabel("0:00")
        self.totalTimeLabel = QLabel("0:00")

        # Set size policies to reduce space
        self.timeline.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.currentTimeLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.totalTimeLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Create a layout for the timeline and labels
        timelineLayout = QHBoxLayout()
        timelineLayout.addWidget(self.currentTimeLabel)
        timelineLayout.addWidget(self.timeline)
        timelineLayout.addWidget(self.totalTimeLabel)

        # Create a main layout
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(timelineLayout)

        # Create a widget for the main window
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Set the video output
        self.mediaPlayer.setVideoOutput(videoWidget)

        # Connect signals for updating the timeline
        self.mediaPlayer.positionChanged.connect(self.update_position)
        self.mediaPlayer.durationChanged.connect(self.update_duration)

        # Create and show the control window
        self.controlWindow = ControlWindow(self)
        self.controlWindow.show()

    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mov)")
        if fileName:
            self.mediaPlayer.setSource(QUrl.fromLocalFile(fileName))

    def play_video(self):
        self.mediaPlayer.play()

    def pause_video(self):
        self.mediaPlayer.pause()
        self.controlWindow.timeCodeLabel.setText(f"Time Code: {self.format_time(self.mediaPlayer.position())}")

    def play_2x(self):
        self.mediaPlayer.setPlaybackRate(2.0)

    def play_5x(self):
        self.mediaPlayer.setPlaybackRate(5.0)

    def play_10x(self):
        self.mediaPlayer.setPlaybackRate(10.0)

    def play_slow(self):
        self.mediaPlayer.setPlaybackRate(0.5)

    def update_position(self, position):
        self.timeline.setValue(position)
        self.currentTimeLabel.setText(self.format_time(position))

    def update_duration(self, duration):
        self.timeline.setRange(0, duration)
        self.totalTimeLabel.setText(self.format_time(duration))

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def format_time(self, ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
