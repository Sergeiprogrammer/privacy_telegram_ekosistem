from flask import Flask, Blueprint , render_template_string
import os
import sqlite3

app = Flask(__name__)

path = "D:\\windos_custom\\messenger\\storage\\sites_storage"

# Получаем список всех сайтов (папок)
sites = [f.name for f in os.scandir(path) if f.is_dir()]

# Создание маршрутов для каждого сайта
for site in sites:
    blueprint = Blueprint(site, __name__, url_prefix=f'/{site}')
    # Read file content outside the function to capture the current file content
    index_file_path = f"{path}\\{site}\\templates\\index.html"
    with open(index_file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    def make_home(file_content):
        def home():
            return render_template_string(file_content)
        return home

    blueprint.route('/')(make_home(file_content))

    # Registering the Blueprint in the application
    app.register_blueprint(blueprint)

@app.route('/')
def home1():
    items = os.listdir(path)
    my_dict = {}
    for item in items:
        description_path = os.path.join(path, item, "description.txt")
        if os.path.isfile(description_path):
            with open(description_path, 'r') as file:
                contents = file.read().strip()
                my_dict[item] = contents

    value = ""
    for i, (key, description) in enumerate(my_dict.items()):
        if i < int(len(sites)):
            value += f"<div onclick=\"location.href='/{key}'\"><strong>{key}</strong><br>{description}</div>\n"

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Website</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .header {
                width: 100%;
                background-color: #333;
                color: white;
                text-align: center;
                padding: 1em 0;
            }
            .content {
                flex-grow: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                padding: 2em;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 1em;
                width: 60%;
                max-width: 800px;
            }
            .grid div {
                background: white;
                border: 1px solid #ccc;
                height: 100px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-size: 1.2em;
                text-align: center;
                padding: 10px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .grid div:hover {
                background-color: #e0e0e0;
            }
            .footer {
                padding: 1em 0;
                text-align: center;
            }
            .button {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .button:hover {
                background-color: #0056b3;
            }
            .ban-button {
                background-color: #dc3545;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                margin-top: 20px;
                text-align: center;
                width: 200px;
            }
            .ban-button:hover {
                background-color: #c82333;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>My Website</h1>
        </div>
        <div class="content">
            <div class="grid">
                {{ value|safe }}
            </div>
        </div>
        <div class="footer">
            <button class="button">Next Page</button>
            <div class="ban-button" onclick="location.href='/ban_list'">
                <strong>бан лист!</strong><br>здесь вся пресональная информация забаненых!
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content, value=value)

@app.route('/ban_list')
def bans():
    conn = sqlite3.connect('D:\\windos_custom\messenger\\telegramm\\ban_list.db')
    # Создаем курсор для выполнения запросов
    cursor = conn.cursor()
    # Создаем таблицу, если она не существует
    cursor.execute(f"SELECT * FROM users")
    value1 = cursor.fetchall()
    html_content1 = """
    <style>
    .ban-button {
                background-color: #0024fa;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                text-align: center;
                width: 200px;
            }
    </style> 
    {{ my_value }}   
    <div class="ban-button" onclick="location.href='/'">
                <strong>бан лист!</strong><br>здесь вся пресональная информация забаненых!               
            </div>
    """
    return render_template_string(html_content1, my_value=value1)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=50100, debug=True, ssl_context="adhoc")