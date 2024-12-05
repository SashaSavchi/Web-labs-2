from flask import Flask, url_for, redirect, render_template, request
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7

import os 

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)

@app.route("/")
@app.route("/index")
def index():
    css_path = url_for("static", filename="lab1/main.css")
    return f'''
        <!doctype html>
        <html>
            <head>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <link rel="stylesheet" href="{css_path}">
            </head>
            <body>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                    <li><a href="/lab3">Третья лабораторная</a></li>
                    <li><a href="/lab4">Четвертая лабораторная</a></li>
                    <li><a href="/lab5">Пятая лабораторная</a></li>
                    <li><a href="/lab6">Шестая лабораторная</a></li>
                    <li><a href="/lab7">Седьмая лабораторная</a></li>
                    <li><a href="/lab8">Восьмая лабораторная</a></li>
                    <li><a href="/lab9">Девятая лабораторная</a></li>
                </ul>
            <footer>
                Цуканова Александра Руслановна, группа ФБИ-21, курс 3, год 2024
            </footer>
            </body>
        </html>'''


@app.errorhandler(404)
def not_found(err):
    css_err = url_for("static", filename="err.css")
    img_err = url_for("static", filename="404.png")
    return f'''
        <!doctype html>
        <html>
            <head>
                <title>Страница не найдена</title>
                <link rel="stylesheet" href="{css_err}">
            </head>
            <body>
                <h1>Страница не найдена</h1>
                <p>К сожалению, запрашиваемая Вами страница не была найдена.</p>
                <p>Вы можете перейти на <a href="/">главную страницу</a> или попробовать воспользоваться поиском.</p>
                <img src="{img_err}">
            </body>
        </html>''', 404


@app.errorhandler(500)
def server_error(err):
    return '''
        <!doctype html>
        <html>
            <head>
                <title>Внутренняя ошибка сервера</title>
            </head>
            <body>
                <h1>Произошла внутренняя ошибка сервера</h1>
                <p>
                    Приносим свои извинения за неудобства. Пожалуйста, попробуйте обновить страницу или вернуться позже.
                </p>
            </body>
        </html>''', 500