from flask import Flask, Blueprint , render_template_string , render_template , url_for , request
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
    with open('address.txt', 'w') as f:
        f.write(request.url_root)
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

    return render_template('index.html', value=value)

@app.route('/youtube1/find', methods=['GET', 'POST'])
def find_youtube():
    message = None
    if request.method == 'POST':
        message = request.form.get('message')
    return render_template('find.html', message=message)

@app.route('/youtube', defaults={'video_path': None})
@app.route('/youtube/<video_path>')
def youtube(video_path):
    folder_path = 'static/video'
    file_name = video_path + ".mp4" if video_path else ""
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(file_path):
        return "Видеофайл не найден", 404

    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Site 1</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #e0f7fa;
                    color: #006064;
                    text-align: center;
                    padding: 50px;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to Site 1!</h1>
            <p>This is the first test site.</p>
            <video width="640" height="480" controls>
                <source src="{{ path }}" type="video/mp4">
            </video>
            <div class="ban-button" onclick="location.href='/'">
                <strong>бан лист!</strong><br>вернуться обратон!
            </div>
        </body>
        </html>
        """
    return render_template_string(html, path=url_for('static', filename='video/' + file_name))

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
    app.run(host="0.0.0.0", port=00000, debug=True, ssl_context="adhoc")