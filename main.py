import json
import multiprocessing

import sys

import telebot
from PyQt6.QtWidgets import QApplication

from MainWindow import MainWindow
from SystemFunctions import get_from_json, resource_path, apps_list, update_json, save_stats_to_file

try:
    bot = telebot.TeleBot(get_from_json(resource_path("jsons/settings.json"))["TOKEN"])
except:pass

commands = [
    telebot.types.BotCommand(command="/add_code", description="Создать код"),
    telebot.types.BotCommand(command="/reset", description="Сбросить статистику"),
    telebot.types.BotCommand(command="/id", description="Получить id"),
    telebot.types.BotCommand(command="/stats", description="Получить статистику")
]

try:
    bot.set_my_commands(commands)
except:pass


def app_exists(app):
    apps = apps_list()
    return app in apps


def add_code(code, app, time):
    update_json(resource_path("jsons/codes.json"), code, {"app": app, "time": time})
    print(get_from_json(resource_path("jsons/codes.json")))


@bot.message_handler(commands=["add_code"])
def add_code_handler_command(message):
    bot.send_message(message.chat.id, "Введите код в формате: код, приложение, время в секундах")
    bot.register_next_step_handler(message, get_code)


def get_code(message):
    text = message.text
    if len(text.split(",")) == 3:
        code, app, time = text.split(",")
        code = code.strip()
        app = app.strip()
        time = time.strip()
        if app_exists(app):
            add_code(code, app, time)
            bot.send_message(message.chat.id, "Код успешно добавлен")
        else:
            bot.send_message(message.chat.id, "Ошибка: такого приложения нет в списке")
    else:
        bot.send_message(message.chat.id, "Ошибка: неверный формат ввода")


@bot.message_handler(commands=["start"])
def start_command(message):
    file = open(resource_path("images/croak-logo300.png"), "rb")

    bot.send_photo(message.chat.id, file,
                   caption=f"Добро пожаловать в Croak! Для настройки зайдите через приложение на компьютере")


@bot.message_handler(commands=["id"])
def id_command(message):
    bot.send_message(message.chat.id, f"Ваш chat_id: {message.chat.id}. Используйте его для привязки приложения")


@bot.message_handler(commands=["stats"])
def stats_command(message):
    settings = get_from_json(resource_path("jsons/settings.json"))
    chat_id = settings["chat_id"]
    if int(message.chat.id) == int(chat_id):
        directory = settings["directory"] + "/Статистика.xlsx"
        stats_apps = get_from_json(resource_path("jsons/stats_apps.json"))
        save_stats_to_file(directory, stats_apps)
        file = open(directory, "rb")
        bot.send_document(chat_id, file)
        file.close()
    else:
        bot.send_message(message.chat.id, f"У вас нет доступа к статистике!")


@bot.message_handler(commands=["reset"])
def reset(message):
    chat_id = get_from_json(resource_path("jsons/settings.json"))["chat_id"]
    if int(message.chat.id) == int(chat_id):
        with open("stats_apps.json", "w") as f:
            json.dump({}, f)
        bot.send_message(message.chat.id, f"Статистика сброшена")
    else:
        bot.send_message(message.chat.id, f"У вас нет доступа к статистике!")


def run_bot():
    bot.polling()


def run_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    multiprocessing.freeze_support()
    open_window_process = multiprocessing.Process(target=run_window)
    try:
        multiprocessing.freeze_support()
        bot_process = multiprocessing.Process(target=run_bot)

        bot_process.start()
    except:
        pass
    open_window_process.start()

    try:
        bot_process.join()
    except:pass
    open_window_process.join()
