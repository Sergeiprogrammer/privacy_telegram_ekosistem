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

file_path = "D:\\windos_custom\\messenger\\"

# Ваш токен, который вы получили от BotFather
TOKEN = 'your_api_token'
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
        FOREIGN KEY (id) REFERENCES users(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings2 (
        id INTEGER,
        saved_contacts TEXT,
        FOREIGN KEY (id) REFERENCES users(id)
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
        list1 = ["/start", "/help", "/start_chat", "/settings", "/create_id", "/internet", "/add_site","/settings"]
        bot.send_message(chat_id,f"доступные функции \n {list1[0]} старт \n {list1[1]} помощь \n {list1[2]} начать перписывать \n {list1[3]} настройки (рекомндуем ознакомисться!) \n {list1[4]} создание id бота (обезательный этап для перписок) \n {list1[5]} выход в приватный интренет тг бота , \n {list1[6]} добавить новый сайт \n")
        markup = types.ReplyKeyboardMarkup()
        markup.row(*(types.KeyboardButton(i) for i in list1))
        bot.send_message(chat_id,"выберите опцию:",reply_markup=markup)
    else:
        bot.send_message(chat_id,"вы забанены")

@bot.message_handler(commands=['internet'])
def internet(message):
    chat_id = message.chat.id
    if info_get(message) == True:
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup()
        web_app_info = types.WebAppInfo(url="https://192.168.1.128:50100")  # Укажите URL вашего веб-приложения
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
        bot.register_next_step_handler(callback.message, alarm)  # <--- Change here
    if callback.data == "contact_panel":
        bot.send_message(chat_id, "введите id человека который будет в быстром меню")
        bot.register_next_step_handler(callback.message, contacts)  # <--- Change here
    if callback.data == "languages":
        print('в разработке')
        pass
        # TODO
@bot.message_handler(commands=["start_chat"])
def start_chat_0(message):
    chat_id = message.chat.id
    if info_get(message) == True:
        if message.text != "/help":
            pass
        else:
            chat_id = message.chat.id
            result = db_action("SELECT bot_id1, bot_id2, bot_id3 FROM users WHERE id =?", (chat_id,) , "bot_id.db")
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
    else:
        bot.send_message(chat_id, "вы забанены")

def start_chat_1(message, result1):
    chat_id = message.chat.id
    if len(message.text) != 16:
        bot.send_message(chat_id,"ошибка id нету")
    else:
        def start_chat_2_wrapper(msg):
            start_chat_2(msg, chat_id, message.text)
        bot.register_next_step_handler(message, start_chat_2_wrapper)
        markup = types.ReplyKeyboardMarkup()
        result = db_action("SELECT saved_contacts FROM settings2 WHERE id = ?" , (chat_id,), "bot_id.db")
        markup.row(*(types.KeyboardButton(i[0]) for i in result))
        bot.send_message(chat_id, "введите id вашего собеседника или выберите из истории" , reply_markup=markup)
def start_chat_2(message, chat_id, result1):
    if message.text == "/cancel":
        bot.send_message(chat_id,"работа отправки сообщение завершена!")
    else:
        try:
            result = db_action("SELECT id FROM users WHERE bot_id1 = ? or bot_id2 = ? or bot_id3 = ?",
                            (message.text, message.text, message.text),"bot_id.db")[0]
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
    if message.text != "/cancel":
        bot.send_message(name, message.text + f" \n отправленно от: {result1}")
        bot.send_message(chat_id, "всё отлично! если хотите продолжить введите новое сообщение иначе введите /cancel")
        def start_chat_3_wrapper(msg):
            start_chat_3(msg, chat_id, (name,), result1)
        bot.register_next_step_handler(message, start_chat_3_wrapper)

@bot.message_handler(commands=["change_id"])
def change_id(message):
    chat_id = message.chat.id
    if info_get(message) == True:
        chat_id = message.chat.id
        bot.send_message(chat_id,"введите id для смены")
        bot.register_next_step_handler(message,change_id_end)
    else:
        bot.send_message(chat_id, "вы забанены")

def change_id_end(message):
    chat_id = message.chat.id
    result = db_action("SELECT bot_id1,bot_id2,bot_id3 FROM users WHERE id = ?", (chat_id,) , "bot_id.db")[0]
    result2 = []
    for i in result:
        if i == message.text:
            i = secrets.token_hex(8)
        result2.append(i)
    print(result2)
    db_action("UPDATE users SET bot_id1 = ?, bot_id2 = ?, bot_id3 = ? WHERE id = ?",(*result2, chat_id) , "bot_id,db")

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
    if step < 3:
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
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте снова.")

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
    # Проверка, есть ли документ в сообщении
    if message.document is None:
        bot.register_next_step_handler(message, add_site)
    else:
        # Проверка размера файла
        if message.document.file_size >= 10485760:  # 10 MB
            bot.send_message(message.chat.id, "нельзя слишком большой файл!")
            bot.register_next_step_handler(message, add_site)
        else:
            file_name = message.document.file_name
            # Проверка расширения файла
            if not file_name.endswith(".zip"):
                bot.send_message(message.chat.id, "файл не zip!")
                bot.register_next_step_handler(message, add_site)
            else:
                # Получение информации о файле
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                # Сохранение файла
                file_path = f"D:\\windos_custom\\messenger\\storage\\user_files\\{message.chat.id}.zip"
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)

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
                        required_files = [f"{sites[0]}description.txt", f"{sites[0]}templates/",
                                          f"{sites[0]}templates/index.html"]
                        for i in required_files:
                            found = False
                            for j in sites:
                                if i.endswith('/'):
                                    # Check if the directory exists
                                    if os.path.dirname(j) == i.rstrip('/'):
                                        found = True
                                        break
                                else:
                                    # Check if the file exists
                                    if j == i:
                                        found = True
                                        break
                            if not found:
                                bot.send_message(message.chat.id,
                                                 f"не хватает следующих файлов: {', '.join(required_files)}")
                            else:
                                zip_ref.extractall(extract_path)
                                bot.send_message(message.chat.id, "сайт проверен и добавлен успешно")
                    shutil.rmtree("D:\\windos_custom\\messenger\\storage\\user_files")
                    os.mkdir("D:\\windos_custom\\messenger\\storage\\user_files")

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
def alarm(message):
    if message.text != "/cancel" and message.text != "/del" and message.text != "/view":
        db_action(f"INSERT INTO settings1 (id, alarm) VALUES (?, ?)", (message.chat.id, message.text), "bot_id.db")
        bot.send_message(message.chat.id,"/cancel - завершить , /del - удалить из контактов , /view - посмотреть контакты")
        bot.register_next_step_handler(message, alarm)
    elif message.text == "/del":
        bot.send_message(message.chat.id,"введите имя контакта для удаления")
        bot.register_next_step_handler(message, delet1)
    elif message.text == "/view":
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup()
        result = db_action(f"SELECT alarm FROM settings1 WHERE id = ?", (chat_id,), "bot_id.db")
        print(result[0])
        markup.row(*(types.KeyboardButton(i) for i in result[0]))
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
        db_action(f"INSERT INTO settings2 (id, saved_contacts) VALUES (?, ?)", (message.chat.id, message.text), "bot_id.db")
        bot.send_message(message.chat.id, "/cancel - завершить , /del - удалить из контактов , /view - посмотреть контакты")
        bot.register_next_step_handler(message, contacts)
    elif message.text == "/del":
        bot.send_message(message.chat.id,"введите имя контакта для удаления")
        bot.register_next_step_handler(message, delet)
    elif message.text == "/view":
        try:
            chat_id = message.chat.id
            markup = types.ReplyKeyboardMarkup()
            result = db_action(f"SELECT saved_contacts FROM settings2 WHERE id = ?", (chat_id,), "bot_id.db")
            print(result[0])
            markup.row(*(types.KeyboardButton(i) for i in result[0]))
            bot.send_message(chat_id, "вот все ваши контакты", reply_markup=markup)
        except:
            chat_id = message.chat.id
            bot.send_message(chat_id,"у вас и так нет контактов")

bot.infinity_polling()