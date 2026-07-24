from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont


class Bubble(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.ToolTip |
            Qt.FramelessWindowHint
        )

        self.setAlignment(Qt.AlignCenter)

        self.setWordWrap(True)

        self.setFont(QFont("Microsoft JhengHei", 10))

        self.setStyleSheet("""
            QLabel{
                background:white;
                color:black;
                border:2px solid #CCCCCC;
                border-radius:12px;
                padding:8px;
            }
        """)

        self.hide()

        self.timer = QTimer()

        self.timer.setSingleShot(True)

        self.timer.timeout.connect(self.hide)

    def showText(self, text, x, y):

        self.setText(text)

        self.adjustSize()

        self.move(
            x,
            y - self.height() - 15
        )

        self.show()

        self.raise_()

        self.timer.start(2000)