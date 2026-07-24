from PySide6.QtCore import (
    QPoint,
    QPropertyAnimation,
    QEasingCurve,
)


class PetAnimation:

    def __init__(self, pet):
        self.pet = pet
        self.jump_anim = None

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