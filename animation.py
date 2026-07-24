from PySide6.QtCore import (
    QPoint,
    QPropertyAnimation,
    QEasingCurve,
    QSequentialAnimationGroup,
)


class PetAnimation:

    def __init__(self, pet):

        self.pet = pet

        self.jump_anim = None

        self.breathe_anim = None

    # ----------------------
    # 跳躍
    # ----------------------

    def jump(self):

        start = self.pet.pos()

        self.jump_anim = QPropertyAnimation(
            self.pet,
            b"pos"
        )

        self.jump_anim.setDuration(450)

        self.jump_anim.setStartValue(start)

        self.jump_anim.setKeyValueAt(
            0.5,
            QPoint(
                start.x(),
                start.y() - 80
            )
        )

        self.jump_anim.setEndValue(start)

        self.jump_anim.setEasingCurve(
            QEasingCurve.OutBounce
        )

        self.jump_anim.start()

    # ----------------------
    # 呼吸
    # ----------------------

    def breathe(self):

        start = self.pet.pos()

        up = QPropertyAnimation(
            self.pet,
            b"pos"
        )

        up.setDuration(1800)

        up.setStartValue(start)

        up.setEndValue(
            QPoint(
                start.x(),
                start.y() - 4
            )
        )

        down = QPropertyAnimation(
            self.pet,
            b"pos"
        )

        down.setDuration(1800)

        down.setStartValue(
            QPoint(
                start.x(),
                start.y() - 4
            )
        )

        down.setEndValue(start)

        self.breathe_anim = QSequentialAnimationGroup()

        self.breathe_anim.addAnimation(up)

        self.breathe_anim.addAnimation(down)

        self.breathe_anim.start()

    # ----------------------
    # 睡覺
    # ----------------------

    def sleep(self):

        if self.breathe_anim is not None:
            self.breathe_anim.stop()

        self.breathe() 