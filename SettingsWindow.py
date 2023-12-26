from PyQt6 import QtGui
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtCore import Qt, QTime, QTimer
from PyQt6.QtGui import QColor, QPainter, QPixmap, QPalette, QBrush
from PyQt6.QtWidgets import QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QFormLayout, QComboBox, QTimeEdit, QTableWidget, QHeaderView, QAbstractItemView, QLCDNumber, QFileDialog, \
    QTableWidgetItem, QColorDialog

from PopUpMessages import pop_up_message
from SystemFunctions import get_from_json, resource_path, apps_list, update_json, delete_from_json, reset_json, \
    save_stats_to_file, format_time

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

        self.time_label = QLabel("Установить лимит времени:", self.page1)
        self.time_spinbox = QTimeEdit()
        self.time_format = "hh:mm"
        self.select_button = QPushButton("Выбрать", self.page1)

        self.time_after_reset = QLabel("Установить время при сбросе и открытии:", self.page1)
        self.time_spinbox_after_reset = QTimeEdit()
        self.time_format = "hh:mm"
        self.select_button_after_reset = QPushButton("Выбрать", self.page1)

        self.password_label = QLabel("Сменить пароль", self.page1)
        self.old_password_edit = QLineEdit(self.page1)
        self.new_password_edit = QLineEdit(self.page1)
        self.change_password_button = QPushButton("Сменить пароль", self.page1)
        directory = get_from_json(resource_path("jsons/settings.json"))["directory"]
        self.directory_label = QLabel(f"Директория для сохранения статистики: {directory}", self.page1)
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
        self.table_apps_limits = QTableWidget()
        self.delete = QPushButton("Удалить лимит")

        # 3 страница

        self.page3_layout = QVBoxLayout()
        self.timer = QLCDNumber()
        self.timer_label = QLabel("Статистика за последние: ")
        self.timer_layout = QHBoxLayout()
        self.chart = QChart()
        self.color_button = QPushButton("Выбрать цвет фона")
        self.series = QPieSeries()
        self.colors = [QColor(55, 192, 203), QColor(102, 205, 170), QColor(220, 20, 60),
                       QColor(72, 61, 139), QColor(0, 128, 128), QColor(119, 136, 153), QColor(139, 69, 19),
                       QColor(75, 0, 130), QColor(240, 230, 140), QColor(255, 20, 147), QColor(135, 206, 235),
                       QColor(250, 235, 215)]

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

        self.time_send_label_time = QLabel(
            f"Время отправки: {(get_from_json(resource_path('jsons/settings.json')))['send_stats_time']}", self.page1)
        self.time_send_label = QLabel("Выбрать время отправки статистики:", self.page1)
        self.time_send_stats = QTimeEdit()
        self.time_send_stats_button = QPushButton("Изменить время отправки")
        self.page5_token_title = QLabel("Вставьте токен вашего бота в телеграм")
        self.page5_token_edit = QLineEdit()
        self.page5_token_button = QPushButton("Подтвердить")
        self.page5_bot_title = QLabel("Получите код из вашего бота по команде /id"
                                      " и впишите его в форму ниже")
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

        self.select_button_after_reset.clicked.connect(self.change_time_after_reset)
        self.select_button.clicked.connect(self.change_time_limit)
        self.change_password_button.clicked.connect(self.change_password)
        self.directory_button.clicked.connect(self.change_directory)

        # 2 страница

        self.set_limit.clicked.connect(self.new_app_limit)
        self.update_limits_apps_table()
        self.delete.clicked.connect(self.delete_clicked_limit)

        # 3 страница

        self.color_button.clicked.connect(self.color_diagram_picker)
        self.reset_button.clicked.connect(self.reset_stats)
        self.update_timer.timeout.connect(self.update_diagram)

        # 4 страница

        self.page4_add.clicked.connect(self.add_code)
        self.page4_total_add.clicked.connect(self.add_total_code)
        self.page4_delete.clicked.connect(self.delete_code)

        # 5 страница
        self.page5_token_button.clicked.connect(self.add_token)
        self.time_send_stats_button.clicked.connect(self.change_send_time)
        self.page5_confirm_button.clicked.connect(self.chat_id_update)
        self.page5_button.clicked.connect(self.save_stats_to_file)
        self.page5_send.clicked.connect(self.main_window.send_stats_file_to_telegram)

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
        self.time_label.setFont(font_h2)
        self.time_label.setStyleSheet("color: rgb(255, 255, 255);")

        self.time_spinbox.setDisplayFormat("hh:mm")
        self.time_spinbox.setTime(QTime(0, 0))

        self.select_button.setFont(font_small_button)
        self.select_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.time_after_reset.setFont(font_h2)
        self.time_after_reset.setStyleSheet("color: rgb(255, 255, 255);")

        self.time_spinbox_after_reset.setDisplayFormat("hh:mm")
        self.time_spinbox_after_reset.setTime(QTime(0, 0))

        self.select_button_after_reset.setFont(font_small_button)
        self.select_button_after_reset.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.total_time = 0

        self.password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_label.setFont(font_h2)
        self.password_label.setStyleSheet("color: rgb(255, 255, 255);")

        self.old_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.change_password_button.setFont(font_small_button)
        self.change_password_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.directory_label.setWordWrap(True)

        self.directory_label.setFont(font_h2)
        self.directory_label.setStyleSheet("color: rgb(255, 255, 255);")

        self.directory_button.setFont(font_small_button)
        self.directory_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.page1_layout.addWidget(self.time_label)
        self.page1_layout.addWidget(self.time_spinbox)
        self.page1_layout.addWidget(self.select_button)
        self.page1_layout.addWidget(self.time_after_reset)
        self.page1_layout.addWidget(self.time_spinbox_after_reset)
        self.page1_layout.addWidget(self.select_button_after_reset)
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

        self.table_apps_limits.setColumnCount(2)
        self.table_apps_limits.setHorizontalHeaderLabels(["Приложение", "Время"])
        self.table_apps_limits.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.table_apps_limits.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_apps_limits.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)
        self.table_apps_limits.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.page2_layout.addWidget(self.table_apps_limits)

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
        self.chart.setBackgroundBrush(self.main_window.color_diagram)

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

        self.load_data_to_table()

    def ui_page5(self):

        self.page5_token_title.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")

        self.page5_token_edit.setFixedSize(800, 30)

        self.page5_token_button.setFont(font_button)
        self.page5_token_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

        self.time_send_label_time.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")

        self.time_send_stats.setDisplayFormat("hh:mm:ss")
        self.time_send_stats.setTime(QTime(0, 0))
        self.page5_bot_title.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")
        self.page5_code_edit.setFixedSize(800, 30)

        self.time_send_stats_button.setFont(font_button)
        self.time_send_stats_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

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

        self.page5_layout.addWidget(self.time_send_label_time)
        self.page5_layout.addWidget(self.time_send_stats)
        self.page5_layout.addWidget(self.time_send_stats_button)
        self.page5_layout.addWidget(self.page5_title)
        self.page5_layout.addWidget(self.page5_button)
        self.page5_layout.addWidget(self.page5_send)
        self.page5_layout.addWidget(self.page5_token_title)
        self.page5_layout.addWidget(self.page5_token_edit)
        self.page5_layout.addWidget(self.page5_token_button)
        self.page5_layout.addWidget(self.page5_bot_title)
        self.page5_layout.addWidget(self.page5_code_edit)
        self.page5_layout.addWidget(self.page5_confirm_button)
        self.page5.setLayout(self.page5_layout)
        self.stackedWidget.addWidget(self.page5)

    # Страница 1

    def change_time_after_reset(self):
        """Выбирает новое время из спинбокса и обновляет настройки

        Атрибуты:
            new_time: строка с новым временем в формате "hh:mm"
            h: часы в новом времени
            m: минуты в новом времени
            self.total_time: общее время в секундах
        """
        time_limit = self.time_spinbox_after_reset.time().toString("hh:mm")
        h, m = time_limit.split(':')
        new_time = int(h) * 3600 + int(m) * 60  # секунд
        if new_time > 0:
            update_json(resource_path("jsons/settings.json"), "total_time_after_reset", new_time)
            self.main_window.update_from_json("total_time_after_reset")
            pop_up_message(text=f"Лимит времени при запуске изменен на: {time_limit}",
                           icon_path=resource_path("images/success2.png"),
                           title="Успешно")
        else:
            pop_up_message(text=f"Лимит не может быть меньше минуты", icon_path=resource_path("images/error3.png"),
                           title="Ошибка")
        self.time_spinbox_after_reset.setTime(QTime(0, 0))

    def change_time_limit(self) -> None:
        """Выбирает новое время из спинбокса и обновляет настройки

        Атрибуты:
            new_time: строка с новым временем в формате "hh:mm"
            h: часы в новом времени
            m: минуты в новом времени
            self.total_time: общее время в секундах
        """
        time_limit = self.time_spinbox.time().toString("hh:mm")
        h, m = time_limit.split(':')
        new_time = int(h) * 3600 + int(m) * 60  # секунд
        if new_time > 0:
            self.total_time = new_time
            update_json(resource_path("jsons/settings.json"), "total_time", self.total_time)
            self.main_window.update_from_json("total_time")
            pop_up_message(text=f"Лимит общего времени изменен на: {time_limit}",
                           icon_path=resource_path("images/success2.png"),
                           title="Успешно")
        else:
            pop_up_message(text=f"Лимит не может быть меньше минуты", icon_path=resource_path("images/error3.png"),
                           title="Ошибка")
        self.time_spinbox.setTime(QTime(0, 0))

    def change_password(self) -> None:
        """Изменяет пароль, если старый пароль совпадает с данными из файла jsons/settings.json

        Аргументы:
            old_password: строка с введенным старым паролем
            new_password: строка с введенным новым паролем
            data: словарь с данными из файла jsons/settings.json
            self.password: строка с новым паролем
        """
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        data = get_from_json(resource_path("jsons/settings.json"))
        if old_password == data["password"]:
            if len(new_password) > 3:
                self.password = new_password
                update_json(resource_path("jsons/settings.json"), "password", self.password)
                pop_up_message(text="Пароль изменен.", icon_path=resource_path("images/success3.png"),
                               title="Успешно")
                self.main_window.update_from_json("password")
            else:
                pop_up_message(text="Длина пароля не может быть меньше 4",
                           icon_path=resource_path("images/error2.png"),
                           title="Ошибка")
        else:
            pop_up_message(text="Неверный старый пароль! Попробуйте еще раз.",
                           icon_path=resource_path("images/error5.png"),
                           title="Ошибка")

    def change_directory(self) -> None:
        """Выбирает директорию для сохранения статистики и обновляет настройки

        Атрибуты:
            self.directory: строка с путем к выбранной директории
        """
        self.directory = QFileDialog.getExistingDirectory(self, "Выберите директорию")
        self.directory_label.setText(f"Директория для сохранения статистики: {self.directory}")
        update_json(resource_path("jsons/settings.json"), "directory", self.directory)
        self.main_window.update_from_json("directory")

    def closeEvent(self, event) -> None:
        """Обрабатывает событие закрытия окна и обновляет настройки

        Аргументы:
            event: объект события
        """
        event.accept()

    # Страница 2

    def new_app_limit(self):
        blocked_app = self.combo.currentText()
        time_limit = self.time.time().toString("hh:mm")
        h, m = time_limit.split(':')
        time_limit = int(h) * 3600 + int(m) * 60
        update_json(resource_path("jsons/blocked_apps.json"), blocked_app, time_limit)
        update_json(resource_path("jsons/blocked_apps_for_percents.json"), blocked_app, time_limit)
        self.update_limits_apps_table()
        self.main_window.update_from_json("blocked_apps")
        pop_up_message(text=f"Лимит для {blocked_app} установлен", icon_path=resource_path('images/success2.png'),
                       title="Успешно")
        self.time.setTime(QTime(0, 0))

    def update_limits_apps_table(self):
        data = get_from_json(resource_path("jsons/blocked_apps.json"))
        self.table_apps_limits.setRowCount(len(data))
        row = 0
        for blocked_app, time_limit in data.items():
            app_item = QTableWidgetItem(blocked_app)
            h, m = divmod(time_limit, 3600)
            m, s = divmod(m, 60)
            time_str = f'{h:02d}:{m:02d}'
            time_item = QTableWidgetItem(time_str)
            self.table_apps_limits.setItem(row, 0, app_item)
            self.table_apps_limits.setItem(row, 1, time_item)
            row += 1

    def delete_clicked_limit(self):
        row = self.table_apps_limits.currentRow()
        if row != -1:
            app = self.table_apps_limits.item(row, 0).text()

            delete_from_json(resource_path("jsons/blocked_apps.json"), app)
            delete_from_json(resource_path("jsons/blocked_apps_for_percents.json"), app)
            self.update_limits_apps_table()
        self.main_window.update_from_json("blocked_apps")

    # Страница 3

    def color_diagram_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.main_window.color_diagram = QBrush(color)
            self.chart.setBackgroundBrush(self.main_window.color_diagram)

    def update_diagram(self):
        stats = get_from_json(resource_path("jsons/stats_apps.json"))
        total_time = sum(stats.values())

        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        seconds = total_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        self.timer.display(time_str)

        self.series.clear()

        for i, (app, time_spend) in enumerate(stats.items()):
            percentage = round(time_spend / total_time * 100, 2)
            self.series.append(f"{app} ({percentage}%)", time_spend)
            self.series.slices()[i].setBrush(self.colors[i % len(self.colors)])

        self.chart.addSeries(self.series)

    def reset_stats(self):
        reset_json(resource_path("jsons/stats_apps.json"))
        self.series.clear()
        self.timer.display("00:00:00")

    # Страница 4

    def add_total_code(self):
        code = self.page4_total_code.text()
        time = self.page4_total_time.time().toString("hh:mm")

        hours, minutes = time.split(":")
        seconds = 0
        hours = int(hours)
        minutes = int(minutes)

        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            seconds = hours * 3600 + minutes * 60

        if code and seconds > 0:
            pop_up_message("Код на общее время добавлен!", title="Успешно",
                           icon_path=resource_path("images/success4.png"))
            update_json(resource_path("jsons/codes.json"), code, {"app": "Общее время", "time": seconds})
            self.page4_total_code.clear()
            self.load_data_to_table()
        else:
            pop_up_message("Код не может быть пустым или добавлять 0", title="Ошибка", icon_path=resource_path("images/error3.png"))
        self.page4_total_time.setTime(QTime(0, 0))  # Устанавливаем начальное время 00:00

    def add_code(self):
        code = self.page4_code.text()
        app = self.page4_apps.currentText()
        time = self.page4_time.time().toString("hh:mm")

        hours, minutes = time.split(":")
        seconds = 0
        hours = int(hours)
        minutes = int(minutes)

        # Перевод времени в секунды
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            seconds = hours * 3600 + minutes * 60

        # Проверяем, что код не пустой
        if code and seconds > 0:
            update_json(resource_path("jsons/codes.json"), code, {"app": app, "time": seconds})
            self.page4_code.clear()
            self.load_data_to_table()
            pop_up_message(f"Код на {app} добавлен!", title="Успешно",
                           icon_path=resource_path("images/success3.png"))
        else:
            pop_up_message("Код не может быть пустым или добавлять 0", title="Ошибка", icon_path=resource_path("images/error3.png"))
        self.page4_time.setTime(QTime(0, 0))

    def delete_code(self):
        row = self.page4_table.currentRow()
        if row != -1:
            code = self.page4_table.item(row, 0).text()
            delete_from_json(resource_path("jsons/codes.json"), code)
            self.load_data_to_table()
        else:
            pop_up_message("Нет выделенной строки", title="Ошибка", icon_path=resource_path("images/error4.png"))

    def load_data_to_table(self):
        data = get_from_json(resource_path("jsons/codes.json"))
        self.page4_table.setRowCount(len(data))
        for i, code in enumerate(data):
            app = data[code]["app"]
            time1 = data[code]["time"]
            code_item = QTableWidgetItem(code)
            app_item = QTableWidgetItem(app)
            time_item = QTableWidgetItem(format_time(time1))
            self.page4_table.setItem(i, 0, code_item)
            self.page4_table.setItem(i, 1, app_item)
            self.page4_table.setItem(i, 2, time_item)

    # Страница 5

    def chat_id_update(self):
        # Получаем код из формы
        code = self.page5_code_edit.text()
        update_json(resource_path("jsons/settings.json"), "chat_id", code)
        self.main_window.update_from_json("chat_id")
        pop_up_message("Код записан", title="Успешно", icon_path=resource_path("images/success4.png"))

    def total_time_counter(self, app_dict):
        total_time = 0
        for app, time in app_dict.items():
            total_time += time
        return total_time

    def save_stats_to_file(self):
        stats = get_from_json(resource_path("jsons/stats_apps.json"))
        save_stats_to_file(self.directory + "/Статистика.xlsx", stats)
        pop_up_message('Статистика сохранена', title="Успешно!")

    def change_send_time(self):
        time_send_stats = self.time_send_stats.time().toString("hh:mm:ss")
        update_json(resource_path("jsons/settings.json"), "send_stats_time", time_send_stats)
        self.main_window.update_from_json("send_stats_time")
        self.time_send_label_time.setText(
            f"Время отправки: {(get_from_json(resource_path('jsons/settings.json')))['send_stats_time']}")
        pop_up_message(text=f"Время автоматической отправки статистики изменено на: {time_send_stats}",
                       icon_path=resource_path("images/success2.png"), title="Успешно")

    def add_token(self):
        token = self.page5_code_edit.text()
        update_json(resource_path("jsons/settings.json"), "TOKEN", token)
        self.main_window.update_from_json("TOKEN")
        pop_up_message("Токен записан", title="Успешно", icon_path=resource_path("images/success2.png"))

