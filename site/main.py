from flask import Flask, Blueprint , render_template_string
import os

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

    with open("D:\\windos_custom\\messenger\\storage\\sites-number.txt", 'r') as file:
        first_line = file.readline().strip()

    value = ""
    for i, (key, description) in enumerate(my_dict.items()):
        if i < int(first_line):
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
            }
            .button:hover {
                background-color: #0056b3;
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
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content, value=value)

if __name__ == '__main__':
    app.run(debug=True)