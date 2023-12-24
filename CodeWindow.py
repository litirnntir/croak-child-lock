from PyQt6 import QtWidgets

from PopUpMessages import pop_up_message
from SystemFunctions import resource_path, get_from_json


class CodeWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle("Введите код")
        self.resize(300, 100)
        self.code_edit = QtWidgets.QLineEdit(self)
        self.code_edit.setPlaceholderText("Введите код здесь")
        self.confirm_button = QtWidgets.QPushButton("Подтвердить", self)
        self.confirm_button.clicked.connect(self.check_code)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.code_edit)
        self.layout.addWidget(self.confirm_button)

    def check_code(self):
        code = self.code_edit.text()
        codes = get_from_json(resource_path("jsons/codes.json"))
        if code in codes:
            pop_up_message(f"Код |{code}| применен", resource_path("images/success6.png"), "Успешно")

        else:
            pop_up_message(f"Код |{code}| не найден", resource_path("images/error6.png"), "Ошибка")
        self.close()
