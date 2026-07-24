from PySide6.QtWidgets import (
    QLabel,
    QMenu,
    QApplication
)

from PySide6.QtGui import (
    QAction,
    QPixmap
)

from PySide6.QtCore import (
    Qt,
    QPoint,
    QTimer
)

import random
import time

import config
from bubble import Bubble
from animation import PetAnimation


class DesktopPet(QLabel):

    def __init__(self):
        super().__init__()

        # 設定
        self.data = config.load()
        self.scale = self.data["scale"]

        # 圖片
        self.original = QPixmap("pet.png")

        # 泡泡
        self.bubble = Bubble()

        # 動畫
        self.animation = PetAnimation(self)

        # 拖曳
        self.dragPos = QPoint()

        # 睡覺
        self.lastInteraction = time.time()
        self.isSleeping = False

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

        # 呼吸動畫
        self.breatheTimer = QTimer()
        self.breatheTimer.timeout.connect(
            self.animation.breathe
        )
        self.breatheTimer.start(3600)
        self.animation.breathe()

        # 睡覺檢查
        self.sleepTimer = QTimer()
        self.sleepTimer.timeout.connect(
            self.checkSleep
        )
        self.sleepTimer.start(1000)

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
    # 滑鼠按下
    # ----------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            # 更新互動時間
            self.lastInteraction = time.time()

            # 醒來
            if self.isSleeping:
                self.isSleeping = False
                self.animation.breathe()

            # 拖曳起點
            self.dragPos = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            # 動畫
            self.animation.jump()

            # 說話
            self.say()

        super().mousePressEvent(event)

    # ----------------------
    # 拖曳
    # ----------------------

    def mouseMoveEvent(self, event):

        if event.buttons() & Qt.LeftButton:

            self.move(
                event.globalPosition().toPoint()
                - self.dragPos
            )

    # ----------------------
    # 放開滑鼠
    # ----------------------

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

            QApplication.quit()

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
    # 睡覺檢查
    # ----------------------

    def checkSleep(self):

        if self.isSleeping:
            return

        # 測試用：30 秒沒互動就睡覺
        if time.time() - self.lastInteraction > 30:

            self.isSleeping = True

            self.animation.sleep()

            self.bubble.showText(
                "Zzz...",
                self.x() + self.width() // 2,
                self.y()
            )

    # ----------------------
    # 關閉時儲存
    # ----------------------

    def closeEvent(self, event):

        self.data["x"] = self.x()
        self.data["y"] = self.y()
        self.data["scale"] = self.scale

        config.save(self.data)

        event.accept()