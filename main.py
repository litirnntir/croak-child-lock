import sys

from PyQt6.QtWidgets import QApplication

from MainWindow import MainWindow


def run_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_window()
