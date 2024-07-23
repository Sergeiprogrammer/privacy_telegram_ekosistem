import telebot
from telebot import types
import sqlite3
import secrets
from virus_check import virus_check
import json
import asyncio
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

file_path = "D:\\windos_custom\\messenger\\"

# Ваш токен, который вы получили от BotFather
TOKEN = '6898197210:AAFMFGS7W9-yWSqYj14enTTswoWZRkSvjz8'
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('bot_id.db')
# Создаем курсор для выполнения запросов
cursor = conn.cursor()
# Создаем таблицу, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        bot_id1 TEXT,
        bot_id2 TEXT,
        bot_id3 TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_preferences (
        original_id INTEGER,
        FOREIGN KEY (original_id) REFERENCES users (id)
    )
''')

conn.commit()
def db_action(query, params):
    conn = sqlite3.connect(f'bot_id.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    if "SELECT" in query:
        return cursor.fetchall()
    conn.commit()
    cursor.close()

@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"доступные функции \n /start старт \n /help помощь \n /start_chat начать перписывать \n /prefernces добавить предпочтение в базу \n /settings настройки \n /create_id создание id бота обезательный этап для перписок \n /internet интренет , /add_site добавить новый сайт")


@bot.message_handler(commands=['internet'])
def internet(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    web_app_info = types.WebAppInfo(url="https://www.youtube.com/")  # Укажите URL вашего веб-приложения
    markup.add(types.KeyboardButton(text='Открыть интернет', web_app=web_app_info))
    bot.send_message(chat_id, "Нажмите на кнопку ниже, чтобы открыть веб-приложение.", reply_markup=markup)

@bot.message_handler(commands=['start'])
def sigma(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("подробней!" , callback_data="help"))
    bot.send_message(chat_id, "привет это конфиденциальная экосистема телеграмма ", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_help(callback):
    if callback.data == "help":
        help(callback.message)

@bot.message_handler(commands=["start_chat"])
def start_chat_0(message):
    chat_id = message.chat.id
    result = db_action("SELECT bot_id1, bot_id2, bot_id3 FROM users WHERE id =?", (chat_id,))
    if result:
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton(result[0][0])
        btn2 = types.KeyboardButton(result[0][1])
        btn3 = types.KeyboardButton(result[0][2])
        markup.add(btn1,btn2,btn3)
        bot.send_message(chat_id, "введите номер id с которого будет сообщение" , reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: start_chat_1(msg, result))
    else:
        bot.send_message(chat_id, "у вас нет id создайте с помощью /create_id")

def start_chat_1(message, result1):
    chat_id = message.chat.id
    if len(message.text) != 16:
        bot.send_message(chat_id,"ошибка id нету")
    else:
        def start_chat_2_wrapper(msg):
            start_chat_2(msg, chat_id, message.text)
        bot.register_next_step_handler(message, start_chat_2_wrapper)
        bot.send_message(chat_id, "введите id вашего собеседника или выберите из истории")

def start_chat_2(message, chat_id, result1):
    if message.text == "/cancel":
        bot.send_message(chat_id,"ок")
    else:
        try:
            result = db_action("SELECT id FROM users WHERE bot_id1 = ? or bot_id2 = ? or bot_id3 = ?",
                            (message.text, message.text, message.text))[0]
            bot.send_message(chat_id, "ввдетие сообщение")
            if len(str(result[0])) > 0:
                def start_chat_3_wrapper(msg):
                    start_chat_3(msg, chat_id, result, result1)
                bot.register_next_step_handler(message, start_chat_3_wrapper)
            else:
                bot.send_message(chat_id, "вы ошиблись id попробуйте снова \n введиет id вашего собеседника")
                bot.register_next_step_handler(message, lambda msg: start_chat_1(msg, result1))
        except:
            bot.send_message(chat_id,"неприавльный id")

def start_chat_3(message, chat_id, result, result1):
    name = result[0]
    bot.send_message(name, message.text + f" \n отправленно от: {result1}")
    bot.send_message(chat_id, "всё отлично! если хотите продолжить введите новое сообщение иначе введите /cancel")
    def start_chat_3_wrapper(msg):
        start_chat_3(msg, chat_id, (name,), result1)
    bot.register_next_step_handler(message, start_chat_3_wrapper)

@bot.message_handler(commands=["change_id"])
def change_id(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"введите id для смены")
    bot.register_next_step_handler(message,change_id_end)

def change_id_end(message):
    chat_id = message.chat.id
    result = db_action("SELECT bot_id1,bot_id2,bot_id3 FROM users WHERE id = ?", (chat_id,))[0]
    result2 = []
    for i in result:
        if i == message.text:
            i = secrets.token_hex(8)
        result2.append(i)
    print(result2)
    db_action("UPDATE users SET bot_id1 = ?, bot_id2 = ?, bot_id3 = ? WHERE id = ?",(*result2, chat_id))


@bot.message_handler(commands=["create_id"])
def create_id(message):
    my_dict = {
        0: 'bot_id1',
        1: 'bot_id2',
        2: 'bot_id3'
    }
    chat_id = message.chat.id
    result = db_action("SELECT bot_id1,bot_id2,bot_id3 FROM users WHERE id =?", (chat_id,))
    print(result)
    print(result[0])
    print(result[0][1])

    if result:  # Check if the result is empty
        bot.send_message(chat_id,"у вас и так есть 3 id")

    else:
        bot.send_message(chat_id, "сейчас вам выдадут ваши 3 ID")
        list_of_ids = [secrets.token_hex(8) for _ in range(3)]
        db_action(f"INSERT INTO users (id, bot_id1, bot_id2, bot_id3) VALUES (?, ?, ?, ?)",
                  (message.chat.id, *list_of_ids))
        bot.send_message(chat_id, "отправленно успешно")

@bot.message_handler(commands=['add_site'])
def add_site(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "пришлите файлы в zip архиве структурированые по принцыпу из примера")
    bot.register_next_step_handler(message,virus_check1)


def virus_check1(message):
    if message.document.file_size >= 10485760:
        bot.send_message(message.chat.id, "нельзя слишком большой файл!")
    file_name = message.document.file_name
    if file_name[-4:]!= ".zip":
        bot.send_message(message.chat.id, "файл не zip!")
    else:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        print(file_info)
        print(file_name)
        with open(file_path+f"storage\\sites_storage\\user_files\\{message.chat.id}.zip", 'wb') as new_file:
            new_file.write(downloaded_file)
        status = virus_check(message.chat_id)
        if status != True:
            print(status)
        else:
            bot.send_message(message.chat_id,"всё хорошо сайт будет опубликован")
            #TODO сделай беарихвацию zip архива
bot.infinity_polling()