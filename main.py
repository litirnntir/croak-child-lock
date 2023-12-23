import multiprocessing

import sys

import telebot
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication

from MainWindow import MainWindow
from SystemFunctions import get_from_json, resource_path

bot = telebot.TeleBot(get_from_json(resource_path("jsons/settings.json"))["TOKEN"])


def run_bot():
    bot.polling()


def stop_bot():
    bot_process.terminate()
    print("Бот остановлен")


def run_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    time_process = multiprocessing.Process(target=run_window)
    multiprocessing.freeze_support()
    bot_process = multiprocessing.Process(target=run_bot)

    bot_process.start()
    time_process.start()

    bot_process.join()
    time_process.join()
