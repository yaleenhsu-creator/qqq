import sys
from PySide6.QtWidgets import QApplication

from pet import DesktopPet


app = QApplication(sys.argv)

pet = DesktopPet()
pet.show()

sys.exit(app.exec())