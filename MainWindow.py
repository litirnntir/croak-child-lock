from CodeWindow import CodeWindow
from SystemFunctions import update_json
import time

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QBrush, QPalette, QPixmap
from PyQt6.QtWidgets import QMainWindow, QInputDialog, QLineEdit
from SystemFunctions import get_from_json, resource_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        update_json(resource_path("jsons/settings.json"), "total_time", 86400)

        settings = get_from_json(resource_path("jsons/settings.json"))
        stats_apps = get_from_json(resource_path("jsons/stats_apps.json"))

        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")

        '''
        ОБЪЯВЛЕНИЕ
        '''
        # элементы
        self.text_active_app = QtWidgets.QLabel(parent=self.centralwidget)
        self.button_settings = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_exit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_add_time = QtWidgets.QPushButton(parent=self.centralwidget)
        self.text_all_time = QtWidgets.QLabel(parent=self.centralwidget)
        self.time_all_time = QtWidgets.QLabel(parent=self.centralwidget)
        self.time_active_app = QtWidgets.QLabel(parent=self.centralwidget)
        self.progress_bar_all_time = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progress_bar_active_app = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.setCentralWidget(self.centralwidget)

        # атрибуты
        self.time_left_block_app = 0  # Осталось времени в приложении
        self.time_spent = 0  # Прошло времени в приложении
        self.stats_apps = stats_apps
        self.timer = QTimer()
        # Из настроек
        self.total_time = settings['total_time']
        self.token = settings["TOKEN"]
        self.password = settings['password']

        self.active_app = self.total_time
        self.total_time_for_percents = self.total_time
        self.blocked_apps = get_from_json(resource_path("jsons/blocked_apps.json"))
        self.blocked_apps_for_percents = get_from_json(
            resource_path("jsons/blocked_apps_for_percents.json"))  # для прогресс бара
        self.flag = True
        self.settings_window = None
        self.code_window = None
        self.directory = None
        self.break_json = None

        '''
        КНОПКИ
        '''
        # self.button_settings.clicked.connect(self.openSettings)
        self.button_add_time.clicked.connect(self.open_code_window)
        # self.timer.timeout.connect(self.update_data)
        self.button_exit.clicked.connect(self.close)

        self.ui()

        self.retranslate_ui(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def ui(self):
        self.setObjectName("Croak")
        self.setFixedSize(840, 580)

        # Фоновое изображение
        background_image = "/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/background.png"
        pix = QPixmap(background_image)
        pal = QPalette()
        pal.setBrush(self.backgroundRole(), QBrush(pix))
        self.setPalette(pal)
        '''
        ЭЛЕМЕНТЫ
        '''
        # text_active_app - текст с активным приложением
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(37)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.text_active_app.setGeometry(QtCore.QRect(70, 230, 371, 61))
        self.text_active_app.setFont(font)
        self.text_active_app.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.text_active_app.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "border-radius: 20px;   ")
        self.text_active_app.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.text_active_app.setObjectName("text_active_app")
        # button_settings - кнопка настроек
        self.button_settings.setGeometry(QtCore.QRect(70, 440, 331, 71))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(23)
        self.button_settings.setFont(font)
        self.button_settings.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "border-radius: 20px;   \n"
                                           "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.83, fx:0.5, fy:0.5, stop:0 rgba(42, 146, 224, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button_settings.setObjectName("button_settings")
        # button_exit - кнопка выход
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(23)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.button_exit.setGeometry(QtCore.QRect(530, 380, 201, 101))
        self.button_exit.setFont(font)
        self.button_exit.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "border-radius: 20px;   \n"
                                       "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.83, fx:0.5, fy:0.5, stop:0 rgba(21, 75, 115, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button_exit.setObjectName("button_exit")
        self.button_add_time.setGeometry(QtCore.QRect(70, 340, 331, 71))
        # button_add_time - кнопка добавить время
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(23)
        self.button_add_time.setFont(font)
        self.button_add_time.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "border-radius: 20px;   \n"
                                           "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.83, fx:0.5, fy:0.5, stop:0 rgba(42, 146, 224, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button_add_time.setObjectName("button_add_time")
        # text_all_time - текст для общего времени
        self.text_all_time.setGeometry(QtCore.QRect(70, 90, 371, 61))
        self.text_all_time.setFont(font)
        self.text_all_time.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.text_all_time.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "border-radius: 20px;   ")
        self.text_all_time.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.text_all_time.setObjectName("text_all_time")
        # time_all_time - общее время
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(37)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.time_all_time.setGeometry(QtCore.QRect(460, 80, 301, 91))
        self.text_all_time.setFont(font)
        self.text_all_time.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.text_all_time.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "border-radius: 20px;   ")
        self.text_all_time.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.text_all_time.setObjectName("text_all_time")
        self.time_all_time = QtWidgets.QLabel(parent=self.centralwidget)
        self.time_all_time.setGeometry(QtCore.QRect(460, 80, 301, 91))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(55)
        self.time_all_time.setFont(font)
        self.time_all_time.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "border-color: rgb(255, 255, 255);\n"
                                         "border-radius: 20px;\n"
                                         "border: 2px solid;\n"
                                         "border-color: rgb(255, 255, 255);")
        self.time_all_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_all_time.setObjectName("time_all_time")
        # time_active_app = время активного приложения
        self.time_active_app.setGeometry(QtCore.QRect(460, 210, 301, 91))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(55)
        self.time_active_app.setFont(font)
        self.time_active_app.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "border-color: rgb(255, 255, 255);\n"
                                           "border-radius: 20px;\n"
                                           "border: 2px solid;\n"
                                           "border-color: rgb(255, 255, 255);")
        self.time_active_app.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_active_app.setObjectName("time_active_app")
        # progress_bar_all_time - прогресс общий
        self.progress_bar_all_time = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progress_bar_all_time.setGeometry(QtCore.QRect(460, 180, 301, 23))
        self.progress_bar_all_time.setProperty("value", 100)
        self.progress_bar_all_time.setTextVisible(True)
        self.progress_bar_all_time.setObjectName("progress_bar_all_time")
        # progress_bar_active_app - прогресс активного
        self.progress_bar_active_app.setGeometry(QtCore.QRect(460, 310, 301, 23))
        self.progress_bar_active_app.setStyleSheet("")
        self.progress_bar_active_app.setProperty("value", 100)
        self.progress_bar_active_app.setTextVisible(False)
        self.progress_bar_active_app.setObjectName("progress_bar_active_app")
        # timer - запуск таймера
        self.timer.start(1000)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Croak - Child Lock"))
        self.text_active_app.setText(_translate("MainWindow", "В активном приложении:"))
        self.button_settings.setText(_translate("MainWindow", "Настройки"))
        self.button_exit.setText(_translate("MainWindow", "Выйти"))
        self.button_add_time.setText(_translate("MainWindow", "Добавить время"))
        self.text_all_time.setText(_translate("MainWindow", "Осталось времени:"))
        self.time_all_time.setText(_translate("MainWindow", time.strftime("%H:%M:%S", time.gmtime(self.total_time))))
        self.time_active_app.setText(
            _translate("MainWindow", time.strftime("%H:%M:%S", time.gmtime(self.total_time))))

    def open_code_window(self):
        self.code_window = CodeWindow(self)
        self.code_window.show()

    def closeEvent(self, event):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Подтверждение выхода")
        dialog.setLabelText("Введите пароль:")
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)

        ok = dialog.exec()
        password = dialog.textValue()

        data = get_from_json(resource_path("jsons/settings.json"))
        print(data)
        if ok and password == data["password"]:
            if self.settings_window:
                self.settings_window.close()
                event.accept()
        else:
            event.ignore()
           # TODO: добавить вывод
        # pop_up_message(text="Неверный пароль! Попробуйте еще раз.", icon_path="incorrect_password.png", title="Ошибка")
