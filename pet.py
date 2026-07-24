from PySide6.QtWidgets import (
    QLabel,
    QMenu
)

from PySide6.QtGui import (
    QAction,
    QPixmap
)

from PySide6.QtCore import (
    Qt,
    QPoint,
    QPropertyAnimation,
    QEasingCurve
)

import random

import config
from bubble import Bubble


class DesktopPet(QLabel):

    def __init__(self):
        super().__init__()

        # 讀取設定
        self.data = config.load()

        self.scale = self.data["scale"]

        # 原始圖片
        self.original = QPixmap("pet.png")

        # 泡泡
        self.bubble = Bubble()

        # 動畫
        self.jumpAnim = None

        # 拖曳
        self.dragPos = QPoint()

        # 台詞
        self.messages = [
            "嘿嘿～",
            "今天也一起加油！",
            "我陪你～",
            "休息一下吧～",
            "我在這裡！",
            "小P報到！",
            "不要一直戳啦🥺",
            "發呆中……",
            "摸摸我～",
            "欸？"
        ]

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.updatePixmap()

        self.move(
            self.data["x"],
            self.data["y"]
        )

            # ----------------------
    # 更新圖片
    # ----------------------

    def updatePixmap(self):

        size = int(280 * self.scale)

        pix = self.original.scaled(
            size,
            size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.setPixmap(pix)
        self.adjustSize()

    # ----------------------
    # 拖曳
    # ----------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragPos = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):

        if event.buttons() & Qt.LeftButton:

            self.move(
                event.globalPosition().toPoint()
                - self.dragPos
            )

    def mouseReleaseEvent(self, event):

        self.data["x"] = self.x()
        self.data["y"] = self.y()

        config.save(self.data)

    # ----------------------
    # 滾輪縮放
    # ----------------------

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:
            self.scale += 0.05
        else:
            self.scale -= 0.05

        self.scale = max(0.4, min(3.0, self.scale))

        self.data["scale"] = self.scale

        config.save(self.data)

        self.updatePixmap()

            # ----------------------
    # 右鍵選單
    # ----------------------

    def contextMenuEvent(self, event):

        menu = QMenu()

        zoomIn = QAction("🔍 放大", self)
        zoomOut = QAction("🔎 縮小", self)
        resetPos = QAction("🏠 重設位置", self)
        quitAction = QAction("❌ 離開", self)

        menu.addAction(zoomIn)
        menu.addAction(zoomOut)
        menu.addSeparator()
        menu.addAction(resetPos)
        menu.addSeparator()
        menu.addAction(quitAction)

        action = menu.exec(event.globalPos())

        if action == zoomIn:

            self.scale = min(3.0, self.scale + 0.1)
            self.updatePixmap()

            self.data["scale"] = self.scale
            config.save(self.data)

        elif action == zoomOut:

            self.scale = max(0.4, self.scale - 0.1)
            self.updatePixmap()

            self.data["scale"] = self.scale
            config.save(self.data)

        elif action == resetPos:

            self.move(200, 200)

            self.data["x"] = 200
            self.data["y"] = 200

            config.save(self.data)

        elif action == quitAction:

            self.close()

    # ----------------------
    # 跳躍動畫
    # ----------------------

    def jump(self):

        start = self.pos()

        self.jumpAnim = QPropertyAnimation(self, b"pos")

        self.jumpAnim.setDuration(450)

        self.jumpAnim.setStartValue(start)

        self.jumpAnim.setKeyValueAt(
            0.5,
            QPoint(start.x(), start.y() - 80)
        )

        self.jumpAnim.setEndValue(start)

        self.jumpAnim.setEasingCurve(
            QEasingCurve.OutBounce
        )

        self.jumpAnim.start()

            # ----------------------
    # 說話
    # ----------------------

    def say(self):

        text = random.choice(self.messages)

        self.bubble.showText(
            text,
            self.x() + self.width() // 2,
            self.y()
        )

    # ----------------------
    # 左鍵互動
    # ----------------------

    def mouseDoubleClickEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.jump()

            self.say()

    # ----------------------
    # 關閉時儲存
    # ----------------------

    def closeEvent(self, event):

        self.data["x"] = self.x()
        self.data["y"] = self.y()
        self.data["scale"] = self.scale

        config.save(self.data)

        event.accept()