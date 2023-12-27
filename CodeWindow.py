from PyQt6 import QtWidgets

from PopUpMessages import pop_up_message
from SystemFunctions import resource_path, get_from_json, update_json, delete_from_json


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
        blocked_apps = get_from_json(resource_path("jsons/blocked_apps.json"))
        if self.main_window.settings_window:
            self.main_window.settings_window.close()
        if code in codes:
            if codes[code]["app"] in blocked_apps:
                time_limit = get_from_json(resource_path("jsons/blocked_apps.json"))[codes[code]["app"]] + codes[code][
                    "time"]
                update_json(resource_path("jsons/blocked_apps.json"), codes[code]["app"], time_limit)
                update_json(resource_path("jsons/blocked_apps_for_percents.json"), codes[code]["app"], time_limit)
                delete_from_json(resource_path("jsons/codes.json"), code)
                self.main_window.update_from_json("blocked_apps")
                pop_up_message(f"Код |{code}| применен", resource_path("images/success6.png"), "Успешно")
            else:
                if codes[code]["app"] == "Общее время":
                    total_time = get_from_json(resource_path("jsons/settings.json"))["total_time"]
                    time_limit = total_time + codes[code]["time"]
                    update_json(resource_path("jsons/settings.json"), "total_time", time_limit)
                    self.main_window.update_from_json("total_time")
                else:
                    pop_up_message(f"Приложение {codes[code]['app']} не заблокировано",
                                   resource_path("images/error6.png"), "Ошибка")
        else:
            pop_up_message(f"Код |{code}| не найден", resource_path("images/error6.png"), "Ошибка")
        self.close()
