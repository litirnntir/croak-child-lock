import multiprocessing
import sys

import telebot
from PyQt6.QtWidgets import QApplication
from sett import TOKEN

from MainWindow import MainWindow

bot = telebot.TeleBot(TOKEN)


def run_bot():
    bot.polling()


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
    bot_process = multiprocessing.Process(target=run_bot)

    bot_process.start()
    time_process.start()

    bot_process.join()
    time_process.join()
