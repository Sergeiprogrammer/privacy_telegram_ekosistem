import time
import telebot
from telebot import types
import sqlite3
import secrets
from virus_check import virus_check
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
import zipfile
import os
import shutil
import re
import logging

file_path = "D:\\windos_custom\\messenger\\"

# Ваш токен, который вы получили от BotFather
TOKEN = 'yourapitoken'
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('bot_id.db')
# Создаем курсор для выполнения запросов
cursor = conn.cursor()
# Создаем таблицу, если она не существует

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name1 TEXT,
        name2 TEXT,
        name3 TEXT,
        bot_id1 TEXT,
        bot_id2 TEXT,
        bot_id3 TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings1 (
        id INTEGER,
        alarm TEXT,
        number_of_id INTEGER,
        FOREIGN KEY (id) REFERENCES users(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings2 (
        id INTEGER ,
        saved_contacts TEXT,
        FOREIGN KEY (id) REFERENCES users(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS allowed_servers (
        id INTEGER NOT NULL UNIQUE,
        link TEXT
    )
''')

conn.commit()
cursor.close()
conn = sqlite3.connect('ban_list.db')
# Создаем курсор для выполнения запросов
cursor = conn.cursor()
# Создаем таблицу, если она не существует
cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER,
                cause TEXT,
                username TEXT,
                full_name TEXT,
                lang TEXT,
                number INTEGER
            )
        ''')
def db_action(query, params , db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    if "SELECT" in query:
        return cursor.fetchall()
    else:
        return False
    cursor.close()

def info_get(message):
    chat_id = message.chat.id
    first = db_action("SELECT * FROM users WHERE id = ? ", (chat_id,), "ban_list.db")
    if len(first) > 0:
        bot.send_message(chat_id, "вы забанены")
        return False
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("/help", callback_data="help"))
        bot.send_message(chat_id,"нажмите кнопку если нужно вернутьсяв список команд",reply_markup=markup)
        return True

@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    first = db_action("SELECT * FROM users WHERE id = ? ", (chat_id,), "ban_list.db")
    if len(first) == 0:
        list1 = ["/start", "/help", "/start_chat", "/settings", "/create_id", "/internet", "/add_site","/developers","/change_id"]
        bot.send_message(chat_id,f"доступные функции \n {list1[0]} старт \n {list1[1]} помощь \n {list1[2]} начать перписывать \n {list1[3]} настройки (рекомндуем ознакомисться!) \n {list1[4]} создание id бота (обезательный этап для перписок) \n {list1[5]} выход в приватный интренет тг бота \n {list1[6]} добавить новый сайт \n {list1[7]} для разработчиков , \n {list1[8]} позволяет сменить свой id и мия пользователя! , ЕСЛИ ХОТИТЕ ПРИНУДИТЕЛЬНО ЗАВЕРШИТЬ ДЕЙСТВИЕ ИСПОЛЬЗУЙТЕ /cancel")
        markup = types.ReplyKeyboardMarkup()
        markup.row(*(types.KeyboardButton(i) for i in list1))
        bot.send_message(chat_id,"выберите опцию:",reply_markup=markup)
    else:
        bot.send_message(chat_id,"вы забанены")

@bot.message_handler(commands=['internet'])
def internet(message):
    chat_id = message.chat.id
    if info_get(message) == True:
        with open('D:\\windos_custom\\messenger\\site\\address.txt', 'r') as f:
            address = f.read().strip()
            print(address)
        print(address)
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup()
        web_app_info = types.WebAppInfo(url=address)  # Укажите URL вашего веб-приложения
        markup.add(types.KeyboardButton(text='Открыть интернет', web_app=web_app_info))
        bot.send_message(chat_id, "Нажмите на кнопку ниже, чтобы открыть веб-приложение.", reply_markup=markup)
        # сделай чтобы в твоём сайте нейрсоеть анализировала запрос пользователя и подбирала лучшие теги по которым искала сайты а для каждого сайта в description.txt можно указываться сови теги
    else:
        bot.send_message(chat_id,"вы забанены")

@bot.message_handler(commands=['start'])
def sigma(message):
    chat_id = message.chat.id
    if info_get(message) == True:
        chat_id = message.chat.id
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("подробней!" , callback_data="help"))
        bot.send_message(chat_id, "привет это конфиденциальная экосистема телеграмма ", reply_markup=markup)
    else:
        bot.send_message(chat_id,"вы забанены")

@bot.callback_query_handler(func=lambda callback: True)
def callback_help(callback):
    chat_id = callback.message.chat.id
    if callback.data == "help":
        help(callback.message)
    if callback.data == "alarm":
        bot.send_message(chat_id, "введите id человека которого уведомит в случаии смены вашего id")
        result = db_action("SELECT saved_contacts FROM settings2 WHERE id = ?", (chat_id,), "bot_id.db")
        try:
            markup = types.ReplyKeyboardMarkup()
            markup.row(*(types.KeyboardButton(i[0]) for i in result[0]))
        except:
            pass
        finally:
            bot.register_next_step_handler(callback.message, alarm)

    if callback.data == "contact_panel":
        bot.send_message(chat_id, "введите id человека который будет в быстром меню")
        bot.register_next_step_handler(callback.message, contacts)
    if callback.data == "languages":
        print('в разработке')
        pass
        # TODO

@bot.message_handler(commands=["start_chat"])
def start_chat_0(message):
    chat_id = message.chat.id
    if info_get(message) == True:
        if message.text != "/start_chat":
            pass
        else:
            chat_id = message.chat.id
            result = db_action("SELECT bot_id1, bot_id2, bot_id3 FROM users WHERE id =?", (chat_id,) , "bot_id.db")
            if result:
                result3 = db_action("SELECT name1, name2 , name3 FROM users WHERE id =?",(chat_id,), "bot_id.db")
                markup = types.ReplyKeyboardMarkup()
                btn1 = types.KeyboardButton(f"{result[0][0]}({result3[0][0]})")
                btn2 = types.KeyboardButton(f"{result[0][1]}({result3[0][1]})")
                btn3 = types.KeyboardButton(f"{result[0][2]}({result3[0][2]})")
                markup.add(btn1,btn2,btn3)
                bot.send_message(chat_id, "введите номер id с которого будет сообщение" , reply_markup=markup)
                bot.register_next_step_handler(message, lambda msg: start_chat_1(msg, result))
            else:
                bot.send_message(chat_id, "у вас нет id создайте с помощью /create_id")
    else:
        bot.send_message(chat_id, "вы забанены")

def start_chat_1(message, result1):
    if message.text != "/cancel" or "/start_chat":
        chat_id = message.chat.id
        message.text = re.sub(r'\([^)]*\)', '', message.text)
        print(result1[0][0])
        print(message.text)
        if message.text in result1[0]:
            if len(message.text) != 16:
                print(message.text)
                bot.send_message(chat_id,"ошибка id нету")
            else:
                print(message.text)
                def start_chat_2_wrapper(msg):
                    start_chat_2(msg, chat_id, message.text)
                bot.register_next_step_handler(message, start_chat_2_wrapper)
                markup = types.ReplyKeyboardMarkup()
                result = db_action("SELECT saved_contacts FROM settings2 WHERE id = ?" , (chat_id,), "bot_id.db")
                markup.row(*(types.KeyboardButton(i[0]) for i in result))
                bot.send_message(chat_id, "введите id вашего собеседника или приглашение в группу!" , reply_markup=markup)
        else:
            bot.send_message(chat_id,"вы не можите отправить сообщение с этого id")
def start_chat_2(message, chat_id, result1):
    if message.text == "/cancel":
        bot.send_message(chat_id,"работа отправки сообщение завершена!")
    else:
        try:
            if "https://t.me/" not in message.text:
                result = db_action("SELECT id FROM users WHERE bot_id1 = ? or bot_id2 = ? or bot_id3 = ?",(message.text, message.text, message.text),"bot_id.db")[0]
            else:
                result = db_action("SELECT id FROM allowed_servers WHERE link = ?", (message.text,) ,"bot_id.db")
                result = result[0]
            bot.send_message(chat_id, "ввдетие сообщение")
            if len(str(result[0])) > 0:
                def start_chat_3_wrapper(msg):
                    start_chat_3(msg, chat_id, result, result1)
                bot.register_next_step_handler(message, start_chat_3_wrapper)
            else:
                bot.send_message(chat_id, "вы ошиблись id попробуйте снова \n введиет id вашего собеседника")
                bot.register_next_step_handler(message, lambda msg: start_chat_2(msg, chat_id, result1))
        except:
            bot.send_message(chat_id, "вы ошиблись id попробуйте снова \n введиет id вашего собеседника")
            bot.register_next_step_handler(message, lambda msg: start_chat_2(msg, chat_id, result1))

def start_chat_3(message, chat_id, result, result1):
    name = result[0]
    result3 = db_action("SELECT name1, bot_id1, name2 , bot_id2 , name3 , bot_id3 FROM users WHERE id =?", (chat_id,), "bot_id.db")
    nick_name = None
    for i in range(len(result3[0])):
        print(result3[0][i])
        if result3[0][i] == result1:
            nick_name = result3[0][i-1]
    print(nick_name)
    if message.text != "/cancel":
        bot.send_message(name, message.text + f" \n отправленно от: {result1}({nick_name})")
        bot.send_message(chat_id, "всё отлично! если хотите продолжить введите новое сообщение иначе введите /cancel")
        def start_chat_3_wrapper(msg):
            start_chat_3(msg, chat_id, (name,), result1)
        bot.register_next_step_handler(message, start_chat_3_wrapper)
    else:
        bot.send_message(chat_id,"опреация завершена")

@bot.message_handler(commands=["change_id"])
def change_id(message):
    if message.text != "/cancel":
        chat_id = message.chat.id
        if info_get(message) == True:
            chat_id = message.chat.id
            bot.send_message(chat_id,"ВЫ уверен что хотите смнить id? если да то введите да если нет то введите /cancel")
            bot.register_next_step_handler(message,change_id_end)
        else:
            bot.send_message(chat_id, "вы забанены")

def change_id_end(message):
    chat_id = message.chat.id
    if message.text != "/cancel" and "да" in message.text:
        result2 = []
        for i in range(3):
            i = secrets.token_hex(8)
            result2.append(i)
        old_ids = db_action("SELECT bot_id1, bot_id2, bot_id3 FROM users WHERE id =?", (chat_id,), "bot_id.db")
        result1 = db_action("SELECT alarm, number_of_id FROM settings1 WHERE id = ?", (chat_id,), "bot_id.db")
        result = []
        print(result1)
        print(len(result1))
        if len(result1) > 1:
            for i in range(len(result1[0])):
                bot.send_message(db_action("SELECT id FROM users WHERE bot_id1 = ? or bot_id2 = ? or bot_id3 = ?",(result1[i][0], result1[i][0], result1[i][0]), "bot_id.db")[0][0],f"пользователь {old_ids[0][result1[i][1]]} сменил id вот его новый id")
            bot.send_message(chat_id, "дейстиве завершено")
            db_action(
                "UPDATE users SET bot_id1 = ?, bot_id2 = ?, bot_id3 = ? WHERE id = ?",
                (*result2, message.chat.id),
                "bot_id.db"
            )
        elif len(result) == 0:
            bot.send_message(chat_id,"у вас нету контактов для уведомления вы уверены что хотите продолжить? напишите да или /cancel")
            bot.register_next_step_handler(message, ready_or_not, result2)
        else:
            bot.send_message(chat_id,f"мы не можем уведомить 1 контакт добавте ещё или уведомте сами {result[0]}")

def ready_or_not(message, result2):
    if message.text.lower() == "да":
        db_action(
                        "UPDATE users SET bot_id1 = ?, bot_id2 = ?, bot_id3 = ? WHERE id = ?",
            (*result2, message.chat.id),
            "bot_id.db"
        )
        bot.send_message(message.chat.id, "ID успешно обновлены.")
    else:
        bot.send_message(message.chat.id, "Обновление ID отменено.")

@bot.message_handler(commands=["create_id"])
def create_id(message):
    chat_id = message.chat.id
    if info_get(message) == True:
        my_dict = {
            0: 'bot_id1',
            1: 'bot_id2',
            2: 'bot_id3'
        }
        if message.text == "/create_id":
            chat_id = message.chat.id
            result = db_action("SELECT bot_id1,bot_id2,bot_id3 FROM users WHERE id =?", (chat_id,) , "bot_id.db")
            if len(result) > 0:
                bot.send_message(chat_id,"у вас и так есть 3 id")
            else:
                chat_id = message.chat.id
                bot.send_message(chat_id, "сейчас вам выдадут ваши 3 ID")
                list_of_ids = [secrets.token_hex(8) for _ in range(3)]
                list_of_names = []
                step = 0
                bot.send_message(chat_id, f"введите имя для 1 id")
                bot.register_next_step_handler(message, input_handler, list_of_names, list_of_ids, step)
    else:
        bot.send_message(chat_id, "вы забанены")

def input_handler(message, list_of_names, list_of_ids, step):
    if step < 3 and message.text != "/cancel":
        list_of_names.append(message.text)
        step += 1
        if step < 3:
            bot.send_message(message.chat.id, f"введите имя для {step + 1} id")
            bot.register_next_step_handler(message, input_handler, list_of_names, list_of_ids, step)
        else:
            chat_id = message.chat.id
            db_action(
                "INSERT INTO users (id, bot_id1, bot_id2, bot_id3, name1, name2, name3) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (chat_id, *list_of_ids, *list_of_names), "bot_id.db")
            bot.send_message(chat_id, "отправленно успешно")
    else:
        bot.send_message(message.chat.id, "Процесс завершён")

@bot.message_handler(commands=['add_site'])
def add_site(message):
    chat_id = message.chat.id
    if info_get(message) == True and message.text == "/add_site":
        chat_id = message.chat.id
        bot.send_message(chat_id, "пришлите файлы в zip архиве структурированые по принцыпу из примера")
        bot.register_next_step_handler(message, virus_check1)
    elif message.text != "/add_site":
        pass
    else:
        bot.send_message(chat_id, "вы забанены")

def virus_check1(message):
    if message.text != "/cancel":
        # Проверка, есть ли документ в сообщении
        if message.document is None:
            bot.send_message(message.chat.id, "Файл не был отправлен")
            return
        # Проверка размера файла
        if message.document.file_size >= 10485760:  # 10 MB
            bot.send_message(message.chat.id, "Файл слишком большой")
            return
        # Получение информации о файле
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # Сохранение файла
        file_path = f"D:\\windos_custom\\messenger\\storage\\user_files\\{message.chat.id}.zip"
        try:
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
        except Exception as e:
            bot.send_message(message.chat.id, "Ошибка при сохранении файла")
            logging.error(f"Ошибка при сохранении файла: {e}")
            return
        # Проверка наличия файла на диске
        if not os.path.exists(file_path):
            bot.send_message(message.chat.id, "Файл не был сохранен")
            return
        # Проверка на вирусы
        status = virus_check(message.chat.id)
        print(status)
        if status is False:
            bot.send_message(message.chat.id, "в вашем файле есть вирысу вы и ваша семья будете забанены!")
            db_action(
                "INSERT INTO users (id, cause, username, full_name, lang, number) VALUES (?, ?, ?, ?, ?, ?)",
                (message.chat.id, "хотел загрузить вирус", message.username, message.first_name + message.last_name, message.lang_code, None), "ban_list.db")

        else:
            bot.send_message(message.chat.id, "всё хорошо сайт будет опубликован после проверки роботом")
            destination_path = "D:\\windos_custom\\messenger\\storage\\sites_storage"
            extract_path = destination_path
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                sites = zip_ref.namelist()
                print(sites[0])
                required_files = ["description.txt", "templates/", "templates/index.html"]
                for i in required_files:
                    found = False
                    for j in sites:
                        if j.endswith(i):
                            found = True
                            break
                    if not found:
                        bot.send_message(message.chat.id, f"не хватает следующих файлов: {', '.join(required_files)}")
                    else:
                        zip_ref.extractall(extract_path)
                        bot.send_message(message.chat.id, "сайт проверен и добавлен успешно")
            shutil.rmtree("D:\\windos_custom\\messenger\\storage\\user_files")
            os.mkdir("D:\\windos_custom\\messenger\\storage\\user_files")
    else:
        bot.send_message(message.chat.id, "процесс завершён")

@bot.message_handler(commands=['settings'])
def settings(message):
    chat_id = message.chat.id
    if info_get(message) == True:
        markup = types.InlineKeyboardMarkup()
        for i , j in zip(["уведомление контактов при смене id","панель контактов","язык"],["alarm","contact_panel","languages"]):
            print(i)
            print(j)
            markup.add(types.InlineKeyboardButton(i, callback_data=j))
        bot.send_message(chat_id, "что вы хотите?", reply_markup=markup)
        bot.send_message(message.chat.id,"после выбора действия сверху можно выбрать одну из команд /cancel - завершить , /del - удалить из контактов , /view - посмотреть контакты")
    else:
        bot.send_message(chat_id, "вы забанены")
#TODO функция не работае тк во первых может хранить только одного любимого пользователя сдлеай чтобы в базе хранился список а код по анологии используй для других callbcak частей насчёт храенния нескольких контктов и id нечего страшного елси они будут записаны не в одной записи а например сначало id и контакт джона потом алисы а потом опять джона! тоесть вмето update юзай INSERT и не парься

def get_next_step(message,name):
    try:
        print(message.chat.id)
        print(name)
        value = int(message.text[0]) - 1
        print(value)
        db_action(f"INSERT INTO settings1 (id, alarm , number_of_id) VALUES (?, ?, ?)", (message.chat.id, name , value), "bot_id.db")
        bot.send_message(message.chat.id,"ВАЖНО именно с этого номера будет оптравлено сообщение о сменене и из новых id именно по этому номеру он возьёться.")
    except:
        bot.send_message(message.chat.id,"ошибка при заполнении формы!")

def alarm(message):
    if message.text != "/cancel" and message.text != "/del" and message.text != "/view":
        chat_id = message.chat.id
        result5 = db_action("SELECT bot_id1, bot_id2, bot_id3 FROM users WHERE id =?", (chat_id,), "bot_id.db")
        if result5:
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton(f"1 id {result5[0][0]}")
            btn2 = types.KeyboardButton(f"2 id {result5[0][1]}")
            btn3 = types.KeyboardButton(f"3 id {result5[0][2]}")
            markup.add(btn1, btn2, btn3)
            bot.send_message(chat_id,"введите номер id которого он получит вот все ваши id",reply_markup=markup)
            bot.register_next_step_handler(message,get_next_step,message.text)
    elif message.text == "/del":
        bot.send_message(message.chat.id,"введите имя контакта для удаления")
        bot.register_next_step_handler(message, delet1)
    elif message.text == "/view":
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup()
        result = db_action(f"SELECT alarm FROM settings1 WHERE id = ?", (chat_id,), "bot_id.db")
        print(result)
        markup.row(*(types.KeyboardButton(i) for i in result))
        bot.send_message(chat_id, "вот все ваши контакты", reply_markup=markup)
    elif message.text == "/cancel":
        bot.send_message(message.chat.id,"добавление успешно завершено")

def delet(message):
    try:
        if message.text != "/cancel":
            db_action(f"DELETE FROM settings2 WHERE saved_contacts =?", (message.text,), "bot_id.db")
            bot.send_message(message.chat.id,"удаление прошло успешно")
            bot.register_next_step_handler(message, delet)
        else:
            bot.send_message(message.chat.id,"удаление завершено")
    except:
        bot.send_message(message.chat.id,"ошибка удаления")

def delet1(message):
    try:
        if message.text != "/cancel":
            db_action(f"DELETE FROM settings1 WHERE alarm =?", (message.text,), "bot_id.db")
            bot.send_message(message.chat.id, "удаление прошло успешно")
            bot.register_next_step_handler(message, delet1)
        else:
            bot.send_message(message.chat.id,"удаление завершено")
    except:
        bot.send_message(message.chat.id,"ошибка удаления")

def view2(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    result = db_action(f"SELECT saved_contacts FROM settings2 WHERE id = ?", (chat_id,), "bot_id.db")
    print(result[0])
    markup.row(*(types.KeyboardButton(i) for i in result[0]))
    bot.send_message(chat_id, "вот все ваши контакты", reply_markup=markup)

def contacts(message):
    if message.text != "/cancel" and message.text != "/del" and message.text != "/view":
        if message.text != "/cancel":
            db_action(f"INSERT INTO settings2 (id, saved_contacts) VALUES (?, ?)", (message.chat.id, message.text), "bot_id.db")
            bot.send_message(message.chat.id, "/cancel - завершить , /del - удалить из контактов , /view - посмотреть контакты")
            bot.register_next_step_handler(message, contacts)
        else:
            bot.send_message(message.chat.id,"добавление завершено")
    elif message.text == "/del":
        if message.text != "/cancel":
            bot.send_message(message.chat.id,"введите имя контакта для удаления")
            bot.register_next_step_handler(message, delet)
        else:
            bot.send_message(message.chat.id,"удаление остановленно")
    elif message.text == "/view":
        if message.text != "/cancel":
            try:
                chat_id = message.chat.id
                markup = types.ReplyKeyboardMarkup()
                result = db_action(f"SELECT saved_contacts FROM settings2 WHERE id = ?", (chat_id,), "bot_id.db")
                print(result)
                markup.row(*(types.KeyboardButton(i) for i in result))
                bot.send_message(chat_id, "вот все ваши контакты", reply_markup=markup)
            except:
                chat_id = message.chat.id
                bot.send_message(chat_id,"у вас и так нет контактов")
        else:
            bot.send_message(message.chat.id,"добавление завершено")

@bot.message_handler(commands=['developers'])
def devloper(message):
    chat_id = message.chat.id
    if info_get(message) == True:
            bot_id = bot.get_me().id
            status = message.chat.type
            if status != "private":
                members = bot.get_chat_administrators(chat_id)
                for member in members:
                    if member.user.id == bot_id:
                        bot.send_message(chat_id,"все процедуры выполнены!")
                        invite_link = bot.export_chat_invite_link(chat_id)
                        print(message)
                        print(invite_link)
                        try:
                            db_action(f"INSERT OR IGNORE INTO allowed_servers (id, link) VALUES (?, ?)" , (chat_id, invite_link) , "bot_id.db")
                            bot.send_message(chat_id, f"ВАЖНО!! запомните эту ссылку {invite_link}  если вы её потеряете то вам придеться удалить бота из админитсраторов и заново добавлять эту ссылку нужно указать в описание или в закрепленном сообщении и пользователи смогут по ней писать сообщения в ваш канал или группу")
                        except:
                            bot.send_message(chat_id,"ваш канал уже есть в базе")


            else:
                bot.send_message(chat_id,"вы сейчас не в канале или группе чтобы добавить бота туда пригласите его на сервер а затем от туда вызовите команду /developers")
    else:
        bot.send_message(chat_id,"вы забанены")

bot.infinity_polling()