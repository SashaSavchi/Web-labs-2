from flask import Blueprint, url_for, redirect, render_template, request
lab1 = Blueprint('lab1',__name__)

# перехватчик ошибки
@lab1.route('/lab1/error')
def error():
    return 1 + '2'


@lab1.route("/lab1")
def lab():
    return '''<!doctype html>
        <html>
            <head>
                <title>Лабораторная 1</title>
            </head>
            <body>
                <p>
                    Flask — фреймворк для создания веб-приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков — минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </p>
                <a href="/">На главную</a>
                <h2>Список роутов</h2>
                <ul>
                    <li><a href="/">Список лабораторных</a></li>
                    <li><a href="/index">Список лабораторных</a></li>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab1/web">Web-сервер на flask</a></li>
                    <li><a href="/lab1/author">Автор лабораторной</a></li>
                    <li><a href="/lab1/oak">Дуб</a></li>
                    <li><a href="/lab1/counter">Счётчик</a></li>
                    <li><a href="/lab1/clear_counter">Очиститель счётчика</a></li>
                    <li><a href="/lab1/info">Информация</a></li>
                    <li><a href="/lab1/created">Код 201</a></li>
                    <li><a href="/lab1/osh">Ошибка 404</a></li>
                    <li><a href="/lab1/request">Ошибка. 400 Bad Request</a></li>
                    <li><a href="/lab1/unauthor">Ошибка. 401 Unauthorized</a></li>
                    <li><a href="/lab1/payment">Ошибка. 402 Payment Required</a></li>
                    <li><a href="/lab1/forbidden">Ошибка. 403 Forbidden</a></li>
                    <li><a href="/lab1/method_na">Ошибка. 405 Method Not Allowed</a></li>
                    <li><a href="/lab1/teapot">Ошибка. 418 Im a teapot</a></li>
                    <li><a href="/lab1/error">Перехват ошибки. 500</a></li>
                    <li><a href="/lab1/about">Кастомный роут</a></li>
                    <li><a href="/lab1/resource">Создание ресурса</a></li>
                </ul>
            </body>
        </html>'''


@lab1.route("/lab1/web")
def web():
    return '''<!doctype html>
        <html>
            <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
            </body>
        </html>''', 200, {
            'X-server': 'sample',
            'Content-Type':'text/plain; charset=utf-8'
            }


@lab1.route("/lab1/author")
def author():
    name = 'Цуканова Александра руслановна'
    group = 'ФБИ-21'
    faculty = 'ФБ'

    return '''<!doctype html>
        <html>
            <body>
                <p>Студент: ''' + name +  '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>'''


@lab1.route("/lab1/oak")
def oak():
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="oak.jpg")
    return f'''
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="{img_path}">
    </body>
</html>
'''


count = 0
@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!DOCTYPE html>
<html>
    <body>
        <p>Сколько раз вы сюда заходили: ''' + str(count) + '''</p>
        <a href="/lab1/clear_counter">Очистить счётчик</a>
    </body>
</html>
'''


@lab1.route('/lab1/clear_counter')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@lab1.route('/lab1/info')
def info():
    return redirect ('/lab1/author')


# @lab1.route('/lab1/created')
# def created():
#     return '''
# <!DOCTYPE html>
# <html>
#     <body>
#         <h1>Создано успешно</h1>
#         <div><i>что-то создано...создано что-то...</i></div>
#     </body>
# </html>
# ''', 201


# страницы с ошибками
@lab1.route('/lab1/request')
def bad_request():
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>400 Bad Request (Неверный запрос)</h1>
        <div>Неправильный синтаксис</div>
    </body>
</html>
''', 400


@lab1.route('/lab1/unauthor')
def unauthorized():
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>401 Unauthorized (Неаутентифицированный)</h1>
        <div>Клиент должен зарегистрироваться</div>
    </body>
</html>
''', 401


@lab1.route('/lab1/payment')
def payment_required():
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>402 Payment Required (Требуется оплата)</h1>
        <div>Необходим цифровой платеж</div>
    </body>
</html>
''', 402


@lab1.route('/lab1/forbidden')
def forbidden():
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>403 Forbidden (Доступ запрещен)</h1>
        <div>Требуется авторизация</div>
    </body>
</html>
''', 403


@lab1.route('/lab1/method_na')
def method_not_allowed():
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>405 Method Not Allowed (Непозволительный метод)</h1>
    </body>
</html>
''', 405


@lab1.route('/lab1/teapot')
def im_a_teapot():
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>418 Im a teapot (Я чайник:)</h1>
        <div>Попытка заварить кофе в чайнике отклонена.</div>
    </body>
</html>
''', 418


# Кастомный роут
@lab1.route('/lab1/about')
def about():
    img_path = url_for("static", filename="pipl.jpg")
    return f'''
<!DOCTYPE html>
<html>
    <head>
        <title>Необходимое нужное</title>
        <style>
            body {{
                text-align: center;
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }}
            pre {{
                display: inline-block;
                margin: 20px;
                text-align: left;
            }}
            img {{
                width: auto;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <h1>Необходимое нужное</h1>
        <pre>
            на белом фоне 
            в белом шуме 
            бегут не оглядываясь
            от неусыпных забот 
            от объятий устали 
            от тоски бушующей
            сбросив с себя опасения мучившие

            пока они молоды 
            поют громко оперы 
            не сбивая движение
            мчащихся встреченных 
            не слышат здоровье
            упрямятся разуму
            но как же им весело 
            обращаются к разному 
            бесцельно рассматривают и освещают
            еле заметное не каждому значимое
            необходимое нужное 

            воскресные дети
            неспешной походкой 
            не страшась больше дыма
            сияют ярко
            освещают 
            сияют ярко 
            освещают 
            необходимое нужное
        </pre>
            <img src="{img_path}">
    </body>
</html>
''', 200, {
        'Content-Language': 'ru',
        'X-CustomHeader-1': 'Written',
        'X-CustomHeader-2': 'earlier',
    }


# Доп задание. Ресурс
resource_exists = False
@lab1.route('/lab1/created')
def create_resource():
    global resource_exists
    if not resource_exists:
        resource_exists = True
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ресурс Создан</title>
        </head>
        <body>
            <h1>Ресурс создан успешно</h1>
            <a href="/lab1/resource">Вернуться к статусу ресурса</a>
        </body>
        </html>
        ''', 201
    else:
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ошибка</title>
        </head>
        <body>
            <h1>Ошибка создания ресурса</h1>
            <p>Ресурс уже создан.</p>
            <a href="/lab1/resource">Вернуться к статусу ресурса</a>
        </body>
        </html>
        ''', 400


@lab1.route('/lab1/delete')
def delete_resource():
    global resource_exists
    if resource_exists:
        resource_exists = False
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ресурс Удалён</title>
        </head>
        <body>
            <h1>Ресурс удалён успешно</h1>
            <a href="/lab1/resource">Вернуться к статусу ресурса</a>
        </body>
        </html>
        ''', 201
    else:
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ошибка</title>
        </head>
        <body>
            <h1>Ошибка удаления ресурса</h1>
            <p>Ресурс отсутствует.</p>
            <a href="/lab1/resource">Вернуться к статусу ресурса</a>
        </body>
        </html>
        ''', 400
   
    
@lab1.route('/lab1/resource')
def resource_status():
    status_message = "ресурс создан" if resource_exists else "ресурс ещё не создан"
    img_path = url_for("static", filename="painter.png")
    return f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Статус Ресурса</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    background-color: white;
                    padding: 50px;
                }}
                h1 {{
                    color: black;
                }}
                img {{
                    margin-top: 40px;
                    width: auto;
                    height: auto;
                }}
                a {{
                    text-decoration: none;
                    color: #007bff;
                    padding: 10px 20px;
                    border: 1px solid #007bff;
                    border-radius: 5px;
                }}
                a:hover {{
                    background-color: #007bff;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <h1>Статус ресурса: <span id="status">{status_message}</span></h1>
            <div>
                <a href="/lab1/created" id="create-btn">Создать ресурс</a>
                <a href="/lab1/delete" id="delete-btn">Удалить ресурс</a>
            </div>
            <div>
                <img src="{img_path}">
            </div>
        </body>
    </html>
    '''