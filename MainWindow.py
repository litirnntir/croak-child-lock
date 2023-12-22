from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtWidgets import QMainWindow
from SystemFunctions import update_json


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui()

    def ui(self):
        self.setObjectName("Croak")
        self.setFixedSize(840, 580)

        background_image = "/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/background.png"
        pix = QPixmap(background_image)
        pal = QPalette()
        pal.setBrush(self.backgroundRole(), QBrush(pix))
        self.setPalette(pal)
