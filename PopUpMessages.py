from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox


def pop_up_message(text="Текст", icon_path=None, title="Уведомление"):
    msg = QMessageBox()
    if icon_path:
        pixmap = QPixmap(icon_path)
        msg.setIconPixmap(pixmap)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.exec()
