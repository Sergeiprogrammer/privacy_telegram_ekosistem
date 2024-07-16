import os
import time
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    path = "D:\\windos_custom\\messenger\\storage\\sites_storage"
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
            value += "<div><strong>{}</strong><br>{}</div>\n".format(key, description)

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