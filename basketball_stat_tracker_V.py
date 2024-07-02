import sys
from PyQt6.QtWidgets import QApplication
from video_player import VideoPlayer

def basketball_stat_tracker_V():
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    basketball_stat_tracker_V()
