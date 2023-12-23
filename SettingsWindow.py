import time

from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QPainter
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtWidgets import QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QFormLayout, QSpinBox, QComboBox, QTimeEdit, QTableWidget, QHeaderView, QAbstractItemView, QLCDNumber, QFileDialog, \
    QApplication

from PopUpMessages import pop_up_message
from SystemFunctions import get_from_json, resource_path, apps_list, update_json

# Шрифт - кнопки
font_button = QtGui.QFont()
font_button.setFamily("Oswald")
font_button.setPointSize(24)
# Шрифт - маленькие кнопки
font_small_button = QtGui.QFont()
font_small_button.setFamily("Oswald")
font_small_button.setPointSize(18)
# Шрифт - заголовок 1
font_h1 = QtGui.QFont()
font_h1.setFamily("Oswald")
font_h1.setPointSize(24)
# Шрифт - заголовок 2
font_h2 = QtGui.QFont()
font_h2.setFamily("Oswald")
font_h2.setPointSize(18)


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.main_window = parent

        settings = get_from_json(resource_path("jsons/settings.json"))

        '''
        ОБЪЯВЛЕНИЕ
        '''
        # элементы интерфейса

        self.button1 = QPushButton('Настройки')
        self.button2 = QPushButton('Лимиты')
        self.button3 = QPushButton('Статистика')
        self.button4 = QPushButton('Коды')
        self.button5 = QPushButton('Отправить')

        self.stackedWidget = QStackedWidget()
        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()
        self.page4 = QWidget()
        self.page5 = QWidget()

        # 1 страница

        self.label1 = QLabel('', self.page1)
        self.time_label = QLabel("Установить лимит времени:", self.page1)
        self.time_spinbox = QTimeEdit()
        self.time_format = "hh:mm"
        self.select_button = QPushButton("Выбрать", self.page1)
        self.password_label = QLabel("Сменить пароль", self.page1)
        self.old_password_edit = QLineEdit(self.page1)
        self.new_password_edit = QLineEdit(self.page1)
        self.change_password_button = QPushButton("Сменить пароль", self.page1)
        self.directory_label = QLabel("Директория для сохранения статистики: Нет", self.page1)
        self.directory_button = QPushButton("Выбрать директорию", self.page1)
        self.page1_layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # 2 страница

        self.page2_layout = QVBoxLayout()
        self.label = QLabel("Добавить лимит на приложение")
        self.combo = QComboBox()
        self.combo = QComboBox()
        self.time = QTimeEdit()
        self.set_limit = QPushButton("Установить лимит")
        self.table = QTableWidget()
        self.delete = QPushButton("Удалить лимит")

        # 3 страница

        self.page3_layout = QVBoxLayout()
        self.timer = QLCDNumber()
        self.timer_label = QLabel("Статистика за последние: ")
        self.timer_layout = QHBoxLayout()
        self.timer_layout = QHBoxLayout()
        self.timer_layout = QHBoxLayout()
        self.chart = QChart()
        self.color_button = QPushButton("Выбрать цвет фона")
        self.series = QPieSeries()
        self.colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255), QColor(255, 255, 0),
                       QColor(0, 255, 255)]

        self.chart_view = QChartView(self.chart)
        self.reset_button = QPushButton("Сбросить статистику")
        self.update_timer = QTimer()

        # 4 страница

        self.page4_layout = QVBoxLayout()
        self.page4_title = QLabel("Коды для дополнительного времени")
        self.page4_subtitle = QLabel("Код для приложения:")
        self.page4_code = QLineEdit()
        self.page4_apps = QComboBox()
        self.page4_time = QTimeEdit()
        self.page4_add = QPushButton("Добавить код")
        self.page4_total_title = QLabel("Код для общего времени")
        self.page4_total_code = QLineEdit()
        self.page4_total_time = QTimeEdit()
        self.page4_total_add = QPushButton("Добавить код")
        self.page4_table = QTableWidget()
        self.page4_delete = QPushButton("Удалить код")

        # 5 страница

        self.page5_bot_title = QLabel("Получите код из бота @croackchildlockbot по команде /id"
                                      "и впишите его в форму ниже")
        self.page5_code_edit = QLineEdit()
        self.page5_confirm_button = QPushButton("Подтвердить")
        self.page5_title = QLabel("Сохранить или отправить статистику")
        self.page5_button = QPushButton("Сохранить статистику в Эксель")
        self.page5_send = QPushButton("Отправить статистику в телеграм")
        self.page5_layout = QVBoxLayout()

        self.vbox = QVBoxLayout()
        # атрибуты

        self.total_time = settings["total_time"]
        self.password = settings["password"]
        self.directory = get_from_json(resource_path("jsons/settings.json"))["directory"]

        self.setLayout(self.vbox)

        self.setWindowTitle('Настройки')
        self.setFixedSize(840, 580)

        self.ui_page1()
        self.ui_page2()
        self.ui_page3()
        self.ui_page4()
        self.ui_page5()
        '''
        КНОПКИ: НАЖАТИЯ
        '''
        # переключение страниц
        self.button1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.button2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.button3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.button4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.button5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))

        # 1 страница

        self.select_button.clicked.connect(self.p1_select_time)
        self.change_password_button.clicked.connect(self.p1_change_password)

        # 2 страница

        # self.set_limit.clicked.connect(self.p2_set_limit_clicked)
        # self.p2_update_table()
        # self.delete.clicked.connect(self.p2_delete_clicked)

        # 3 страница

        # self.color_button.clicked.connect(self.p3_color_picker)
        # self.reset_button.clicked.connect(self.p2_reset_stats)
        # self.update_timer.timeout.connect(self.p3_update_data)

        # 4 страница

        # self.page4_add.clicked.connect(self.p4_add_code)
        # self.page4_total_add.clicked.connect(self.p4_add_total_code)
        # self.page4_delete.clicked.connect(self.p4_delete_code)

        # 5 страница

        # self.page5_confirm_button.clicked.connect(self.p5_confirm)
        # self.page5_button.clicked.connect(self.p5_save_stats_to_file)
        # self.page5_send.clicked.connect(self.main_window.send_file_to_telegram)

        # Дизайн
        self.ui()

        self.show()

    def ui(self):
        # Фон
        background_image = resource_path("images/background_settings.png")
        pix = QPixmap(background_image)
        pal = QPalette()
        pal.setBrush(self.backgroundRole(), QBrush(pix))
        self.setPalette(pal)
        # Кнопка Настройки
        self.button1.setFont(font_button)
        self.button1.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        # Кнопка Лимиты
        self.button2.setFont(font_button)
        self.button2.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        # Кнопка Статистика
        self.button3.setFont(font_button)
        self.button3.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        # Кнопка коды
        self.button4.setFont(font_button)
        self.button4.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        # Кнопка отправить
        self.button5.setFont(font_button)
        self.button5.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)
        self.stackedWidget.addWidget(self.page4)
        self.stackedWidget.addWidget(self.page5)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.button1)
        self.hbox.addWidget(self.button2)
        self.hbox.addWidget(self.button3)
        self.hbox.addWidget(self.button4)
        self.hbox.addWidget(self.button5)

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.stackedWidget)

    def ui_page1(self):
        self.time_label.setFont(font_h1)
        self.time_label.setStyleSheet("color: rgb(255, 255, 255);")

        self.time_spinbox.setDisplayFormat("hh:mm")
        self.time_spinbox.setTime(QTime(0, 0))

        # self.time_spinbox.setRange(0, 1440)  # Минуты в сутках
        # self.time_spinbox.setSuffix(" минут")
        # self.time_spinbox.setSingleStep(15)
        # self.time_spinbox.setValue(0)
        self.select_button.setFont(font_button)
        self.select_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.total_time = 0

        self.password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_label.setFont(font_h1)
        self.password_label.setStyleSheet("color: rgb(255, 255, 255);")

        self.old_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.change_password_button.setFont(font_button)
        self.change_password_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.directory_label.setWordWrap(True)

        self.directory_label.setFont(font_h1)
        self.directory_label.setStyleSheet("color: rgb(255, 255, 255);")

        self.directory_button.setFont(font_button)
        self.directory_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page1_layout.addWidget(self.time_label)
        self.page1_layout.addWidget(self.time_spinbox)
        self.page1_layout.addWidget(self.select_button)
        self.page1_layout.addWidget(self.password_label)
        self.page1_layout.addStretch()
        self.form_layout.setContentsMargins(0, 0, 20, 20)
        self.form_layout.addRow("Введите старый пароль", self.old_password_edit)
        self.form_layout.addRow("Введите новый пароль", self.new_password_edit)
        self.form_layout.labelForField(self.old_password_edit).setStyleSheet(
            "color: white; font-size: 18px; font-family: Oswald;")
        self.form_layout.labelForField(self.new_password_edit).setStyleSheet(
            "color: white; font-size: 18px; font-family: Oswald;")

        self.page1_layout.addLayout(self.form_layout)
        self.page1_layout.addWidget(self.change_password_button)
        self.page1_layout.addWidget(self.directory_label)
        self.page1_layout.addWidget(self.directory_button)
        self.page1.setLayout(self.page1_layout)

    def ui_page2(self):
        self.label.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")
        self.page2_layout.addWidget(self.label)

        self.combo.addItems(apps_list())
        self.page2_layout.addWidget(self.combo)

        self.time.setDisplayFormat("hh:mm")
        self.time.setTime(QTime(0, 0))
        self.page2_layout.addWidget(self.time)

        self.set_limit.setFont(font_button)
        self.set_limit.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page2_layout.addWidget(self.set_limit)

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Приложение", "Время"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.page2_layout.addWidget(self.table)

        self.delete.setFont(font_button)
        self.delete.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page2_layout.addWidget(self.delete)

        self.page2.setLayout(self.page2_layout)

    def ui_page3(self):
        self.page3.setLayout(self.page3_layout)

        self.timer.setDigitCount(8)
        self.timer.display("00:00:00")

        self.timer_label.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")

        self.timer_layout.addWidget(self.timer_label)
        self.timer_layout.addWidget(self.timer)

        self.page3_layout.addLayout(self.timer_layout)

        self.chart.setTitle("Диаграмма")
        self.chart.setTitleFont(font_h1)

        self.color_button.setFont(font_button)
        self.color_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page3_layout.addWidget(self.color_button)

        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.page3_layout.addWidget(self.chart_view)

        self.reset_button.setFont(font_button)
        self.reset_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page3_layout.addWidget(self.reset_button)

        self.update_timer.start(1000)

    def ui_page4(self):
        self.page4_title.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")
        self.page4_layout.addWidget(self.page4_title)

        self.page4_subtitle.setStyleSheet("color: white; font-size: 18px; font-family: Oswald;")
        self.page4_layout.addWidget(self.page4_subtitle)

        self.page4_code.setPlaceholderText("Введите код")
        self.page4_layout.addWidget(self.page4_code)

        self.page4_apps.addItems(apps_list())
        self.page4_layout.addWidget(self.page4_apps)

        self.page4_time.setDisplayFormat("hh:mm")
        self.page4_time.setTime(QTime(0, 0))  # Устанавливаем начальное время 00:00
        self.page4_layout.addWidget(self.page4_time)

        self.page4_add.setFont(font_small_button)
        self.page4_add.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page4_layout.addWidget(self.page4_add)

        self.page4_total_title.setStyleSheet("color: white; font-size: 18px; font-family: Oswald;")
        self.page4_layout.addWidget(self.page4_total_title)

        self.page4_total_code.setPlaceholderText("Введите код")
        self.page4_layout.addWidget(self.page4_total_code)

        self.page4_total_time.setDisplayFormat("hh:mm")
        self.page4_total_time.setTime(QTime(0, 0))  # Устанавливаем начальное время 00:00
        self.page4_layout.addWidget(self.page4_total_time)

        self.page4_total_add.setFont(font_small_button)
        self.page4_total_add.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page4_layout.addWidget(self.page4_total_add)

        self.page4_table.setColumnCount(3)
        self.page4_table.setHorizontalHeaderLabels(["Код", "Приложение", "Время"])
        self.page4_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.page4_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.page4_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)
        self.page4_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.page4_table.verticalHeader().hide()
        self.page4_table.setRowCount(0)
        self.page4_layout.addWidget(self.page4_table)

        self.page4_delete.setFont(font_small_button)
        self.page4_delete.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.page4_layout.addWidget(self.page4_delete)

        self.page4.setLayout(self.page4_layout)

        # self.p4_load_data()

    def ui_page5(self):
        self.page5_bot_title.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")
        self.page5_code_edit.setFixedSize(800, 50)

        self.page5_confirm_button.setFont(font_button)
        self.page5_confirm_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page5_title.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")

        self.page5_button.setFont(font_button)
        self.page5_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page5_send.setFont(font_button)
        self.page5_send.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page5_layout.addWidget(self.page5_title)
        self.page5_layout.addWidget(self.page5_button)
        self.page5_layout.addWidget(self.page5_send)
        self.page5_layout.addWidget(self.page5_bot_title)
        self.page5_layout.addWidget(self.page5_code_edit)
        self.page5_layout.addWidget(self.page5_confirm_button)
        self.page5.setLayout(self.page5_layout)
        self.stackedWidget.addWidget(self.page5)

    def p1_select_time(self):
        new_time = self.time_spinbox.time().toString("hh:mm")
        h, m = new_time.split(':')
        self.total_time = int(h) * 3600 + int(m) * 60  # секунд
        update_json(resource_path("jsons/settings.json"), "total_time", self.total_time)
        self.main_window.update_settings()
        pop_up_message(text=f"Лимит общего времени изменен на: {new_time} установлен", icon_path="check_icon.png",
                       title="Успешно")

    def p1_change_password(self):
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        data = get_from_json(resource_path("jsons/settings.json"))
        if old_password == data["password"]:
            self.password = new_password
            update_json(resource_path("jsons/settings.json"), "password", self.password)
            pop_up_message(text="Пароль изменен.", icon_path="correct_password.png", title="Успешно")
            self.main_window.update_settings()
        else:
            pop_up_message(text="Неверный пароль! Попробуйте еще раз.", icon_path="incorrect_password.png",
                           title="Ошибка")

    def p1_select_directory(self):
        self.directory = QFileDialog.getExistingDirectory(self, "Выберите директорию")
        self.directory_label.setText(f"Директория для сохранения статистики: {self.directory}")
        update_json(resource_path("jsons/settings.json"), "directory", self.directory)
        self.main_window.update_settings()

    def closeEvent(self, event):
        self.main_window.update_settings()
        event.accept()