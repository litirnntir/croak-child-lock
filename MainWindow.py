import telebot

from CodeWindow import CodeWindow
from PopUpMessages import pop_up_message
from SettingsWindow import SettingsWindow
from SystemFunctions import update_json, close_app, send_notification, get_open_apps, reset_json
import time

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QBrush, QPalette, QPixmap
from PyQt6.QtWidgets import QMainWindow, QInputDialog, QLineEdit
from SystemFunctions import get_from_json, resource_path, get_active_app_name

bot = telebot.TeleBot(get_from_json(resource_path("jsons/settings.json"))["TOKEN"])
no_blocked_list = ["pycharm", "python", "Croak - Child Lock", "Finder", "Croak", "Python"]


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
        # элементы интерфейса
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
        self.chat_id = settings['chat_id']
        self.send_stats_time = settings['send_stats_time']
        self.directory = settings['directory']

        self.active_app = self.total_time
        self.total_time_for_percents = self.total_time
        self.blocked_apps = get_from_json(resource_path("jsons/blocked_apps.json"))
        self.blocked_apps_for_percents = get_from_json(
            resource_path("jsons/blocked_apps_for_percents.json"))  # для прогресс бара
        # self.flag = True
        self.settings_window = None
        self.code_window = None
        self.break_json = None

        '''
        КНОПКИ
        '''
        self.button_settings.clicked.connect(self.open_settings)
        self.button_add_time.clicked.connect(self.open_code_window)
        self.timer.timeout.connect(self.update_data)
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

    def retranslate_ui(self, MainWindow) -> None:
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

    def open_code_window(self) -> None:
        """
        Открывает окно для ввода кода.
        :return: None
        """
        self.code_window = CodeWindow(self)
        self.code_window.show()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Обрабатывает событие закрытия главного окна.
        :param event: событие закрытия
        :return: None
        """
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Подтверждение выхода")
        dialog.setLabelText("Введите пароль:")
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)

        ok = dialog.exec()
        password = dialog.textValue()

        data = get_from_json(resource_path("jsons/settings.json"))
        if ok and password == data["password"]:
            if self.settings_window:
                self.settings_window.close()
            event.accept()
        else:
            event.ignore()
            pop_up_message(text="Неверный пароль! Попробуйте еще раз.",
                           icon_path=resource_path("images/incorrect_password.png.png"),
                           title="Ошибка")

    def open_settings(self) -> None:
        """
        Открывает окно настроек приложения.
        :return: None
        """
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Подтверждение выхода")
        dialog.setLabelText("Введите пароль:")
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
        ok = dialog.exec()
        password = dialog.textValue()

        data = get_from_json(resource_path("jsons/settings.json"))
        if ok and password == data["password"]:
            self.settings_window = SettingsWindow(self)
            self.settings_window.show()
        else:
            pop_up_message(text="Неверный пароль! Попробуйте еще раз.",
                           icon_path=resource_path("images/incorrect_password.png.png"),
                           title="Ошибка")

    def update_from_json(self, param):
        """Обновляет настройки из файла jsons/settings.json"""
        data = get_from_json(resource_path("jsons/settings.json"))
        if param == "password": self.password = data["password"]
        if param == "total_time" or "total_time_for_percents":
            self.total_time = data["total_time"]
            self.total_time_for_percents = data["total_time"]
        if param == "directory": self.directory = data["directory"]
        if param == "chat_id": self.chat_id = data["chat_id"]
        if param == "send_stats_time": self.send_stats_time = data["send_stats_time"]
        if param == "blocked_apps" or "blocked_apps_for_percents":
            self.password = get_from_json(resource_path("jsons/blocked_apps.json"))
            self.blocked_apps_for_percents = get_from_json(
                resource_path("jsons/blocked_apps_for_percents.json"))  # для прогресс бара

    def send_file_to_telegram(self, file: str = "Статистика.xlsx") -> None:
        """Отправляет файл в телеграм по chat_id

        Аргументы:
            file: имя файла, по умолчанию "Статистика.xlsx"
        """
        # Открываем файл excel в режиме чтения
        print(self.directory)
        file = open(resource_path(self.directory + "/" + file), "rb")
        # Отправляем файл по chat_id
        bot.send_document(self.chat_id, file)
        # Закрываем файл
        file.close()

    def send_to_telegram(self, text="Текст") -> None:
        """Отправляет текстовое сообщение в телеграм по chat_id

        Аргументы:
            text: текст сообщения, по умолчанию "Текст"
        """
        bot.send_message(self.chat_id, text)

    def update_data(self) -> None:
        """Главная функция обработки действий"""
        try:
            # TODO: проверка на взлом файла
            utc_time = time.gmtime()  # текущее время, не зависит от устройства
            gmt4_time = time.gmtime(time.mktime(utc_time) + 8 * 3600)  # GMT+4

            # В определенное время сброс статистики, времени и отправка в телеграм
            if self.send_stats_time == time.strftime("%H:%M:%S", gmt4_time):
                self.send_file_to_telegram("Статистика.xlsx")
                update_json(resource_path("jsons/settings.json"), "total_time",
                            24 * 60 * 60)  # обновляем на 24 часа в нужное время
                reset_json(resource_path("jsons/stats_apps.json"))
            # Меняем активное приложение
            new_current_app = get_active_app_name()
            print(new_current_app)
            print(get_from_json("jsons/blocked_apps.json"))
            self.text_active_app.setText(f"В {new_current_app}:")

            # Если время не вышло
            if self.total_time > 0:
                self.total_time -= 1
                # Если приложение изменилось
                if new_current_app != self.active_app:
                    # Если время в приложении больше нуля секунд
                    if self.time_spent > 0:
                        self.stats_apps = get_from_json(resource_path("jsons/stats_apps.json"))
                        # Записываем значение времени в предыдущем приложении
                        if self.active_app in self.stats_apps:
                            update_json(resource_path("jsons/stats_apps.json"), self.active_app,
                                        self.stats_apps[self.active_app] + self.time_spent)
                        else:
                            update_json(resource_path("jsons/stats_apps.json"), self.active_app, self.time_spent)
                    # Обнуляем время в текущем приложении
                    self.time_spent = 0
                    # Обновляем значение в файле, если предыдущее заблокировано
                    if self.active_app in self.blocked_apps:
                        update_json(resource_path("jsons/stats_apps.json"), self.active_app, self.time_left_block_app)
                    # Обновляем текущее приложение
                    self.active_app = new_current_app
                    # Если текущее зблокировано, проверяем, осталось ли время. Если не осталось - закрываем
                    if self.active_app in self.blocked_apps:
                        if self.blocked_apps[self.active_app] <= 1:
                            close_app(new_current_app)
                            self.time_left_block_app = 0  # обнуляем время
                            send_notification(
                                f"Время {new_current_app} вышло. Вы больше не можете находиться в приложении")
                        else:
                            self.time_left_block_app = self.blocked_apps[new_current_app]
                            self.time_left_block_app -= 1
                    else:
                        self.time_left_block_app = self.total_time
                # Если текущее приложение не поменялось
                else:
                    self.time_spent += 1
                    # Если заблокировано, проверяем время
                    if new_current_app in self.blocked_apps:
                        if self.time_left_block_app <= 1:
                            close_app(new_current_app)
                            self.time_left_block_app = 0
                            send_notification(
                                f"Время {new_current_app} вышло. Вы больше не можете находиться в приложении")
                        else:
                            self.time_left_block_app -= 1
                    # Если не заблокировано - ставим общее время как оставшееся
                    else:
                        self.time_left_block_app = self.total_time

                # Меняем время в интерфейсе
                self.time_all_time.setText(time.strftime("%H:%M:%S", time.gmtime(self.total_time)))
                self.time_active_app.setText(time.strftime("%H:%M:%S", time.gmtime(self.time_left_block_app)))

                # Прогресс бар
                if self.active_app in self.blocked_apps and self.time_left_block_app < self.total_time:
                    if self.time_left_block_app > 1:
                        self.progress_bar_active_app.setProperty("value", 100 * self.time_left_block_app /
                                                                 self.blocked_apps_for_percents[self.active_app])
                    else:
                        self.progress_bar_active_app.setProperty("value", 0)
                else:
                    self.progress_bar_active_app.setProperty("value",
                                                             100 * self.total_time / self.total_time_for_percents)
                self.progress_bar_all_time.setProperty("value", 100 * self.total_time / self.total_time_for_percents)

            else:
                if new_current_app != "Python" and new_current_app != "pycharm" and new_current_app != "Croak - Child Lock":
                    send_notification(f"Общее время вышло. Вы больше не можете зайти в {new_current_app}")
                    close_app(new_current_app)
                    apps_list = get_open_apps()
                    for app in no_blocked_list:
                        if app in apps_list: apps_list.remove(app)
                    for application in apps_list:
                        close_app(application)

        except:pass
