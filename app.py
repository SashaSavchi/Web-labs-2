from flask import Flask, url_for, redirect, render_template
app = Flask(__name__)

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


# перехватчик ошибки
@app.route('/lab1/error')
def error():
    return 1 + '2'
#Конкатенация числа и строки вызовет ошибку на сервере
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
# ошибки
# @app.errorhandler(400)
# def bad_request(err):
#     return "400 Bad Request", 400

# @app.errorhandler(401)
# def unauthorized(err):
#     return "401 Unauthorized", 401

# @app.errorhandler(402)
# def payment_required(err):
#     return "402 Payment Required", 402

# @app.errorhandler(403)
# def forbidden(err):
#     return "403 Forbidden", 403

# @app.errorhandler(405)
# def method_not_allowed(err):
#     return "405 Method Not Allowed", 405

# @app.errorhandler(418)
# def im_a_teapot(err):
#     return "418 I'm a teapot", 418


@app.route("/")
@app.route("/index")
def index():
    css_path = url_for("static", filename="main.css")
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
                </ul>
            <footer>
                Цуканова Александра Руслановна, группа ФБИ-21, курс 3, год 2024
            </footer>
            </body>
        </html>'''


@app.route("/lab1")
def lab1():
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


@app.route("/lab1/web")
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


@app.route("/lab1/author")
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


@app.route("/lab1/oak")
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
@app.route('/lab1/counter')
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

@app.route('/lab1/clear_counter')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@app.route('/lab1/info')
def info():
    return redirect ('/lab1/author')


# @app.route('/lab1/created')
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
@app.route('/lab1/request')
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

@app.route('/lab1/unauthor')
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

@app.route('/lab1/payment')
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

@app.route('/lab1/forbidden')
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

@app.route('/lab1/method_na')
def method_not_allowed():
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>405 Method Not Allowed (Непозволительный метод)</h1>
    </body>
</html>
''', 405

@app.route('/lab1/teapot')
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
@app.route('/lab1/about')
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

@app.route('/lab1/created')
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

@app.route('/lab1/delete')
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
    
@app.route('/lab1/resource')
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


# Лаборпаторная 2
@app.route('/lab2/a/')
def a():
    return render_template("base.html", 
                           lab='Лабораторная работа 2', 
                           main_content='со слэшем')

@app.route('/lab2/a')
def a2():
    return render_template("base.html", 
                           lab='Лабораторная работа 2', 
                           main_content='без слэша')

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')


flower_list = ['роза','тюльпан','незабудка','ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flower(flower_id):
    if flower_id >= len(flower_list):
        return render_template("base.html", 
                            lab='Лабораторная работа 2', 
                            main_content='такого цветка нет'), 404 
    else:
        return render_template("base.html", 
                           lab='Лабораторная работа 2', 
                           main_content=f'''
                           <h1>Цветок: {flower_list[flower_id]}</h1>
                           <a href="/lab2/all_flowers">Все цветы</a>''')

@app.route('/lab2/add_flower/', defaults={'name': ''})
# запрос по адресу /lab2/add_flower/ ожидал, что после /add_flower/ 
# будет следовать значение для параметра <name>. Тк это значение отсутствовало, возникал ответ 404.
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if name == '':
        return render_template("base.html", 
                    lab='Лабораторная работа 2', 
                    main_content='Вы не задали имя цветка'), 400
    elif name not in flower_list:
        flower_list.append(name)
        return render_template("base.html", 
                    lab='Лабораторная работа 2', 
                    main_content=f'''
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name} </p>
            <p>Всего цветов: {len(flower_list)}</p>
            <p>Полный список: {flower_list}</p>''')
    else:
        return render_template("base.html", 
                    lab='Лабораторная работа 2', 
                    main_content=f'''
            <h1>Такой цветок уже есть в списке.</h1>
            <a href="/lab2/all_flowers">Полный список</a>'''), 400

@app.route('/lab2/all_flowers')
def all_flowers():
    flowers_html = '<ul>'
    for flower in flower_list:
        flowers_html += f'<li>{flower}</li>'
    flowers_html += '</ul>'
    return render_template("base.html", 
                    lab='Лабораторная работа 2', 
                    main_content=f'''
            <h1>Все цветы</h1>
            {flowers_html}
            <p>Всего цветов: {len(flower_list)}</p>
            <p><a href="/lab2/add_flower/">Добавить цветок</a></p>
            <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>'''), 400


@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return render_template("base.html", 
                    lab='Лабораторная работа 2', 
                    main_content='''<h1>Список цветов очищен</h1>
        <a href="/lab2/all_flowers">Все цветы</a>''')


@app.route('/lab2/example')
def example():
    name, number_l, group, course ='Александра Цуканова', 2, 'ФБИ-21', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', 
                           number_l=number_l, name=name, group=group, 
                           course=course, fruits=fruits)


@app.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', phrase = phrase)


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template("base.html", 
                    lab='Лабораторная работа 2', 
                    main_content=f'''        
            <h1>Расчёт с параметрами</h1>
            <p>Сложение: {a} + {b} = {a + b}</p>
            <p>Вычитание: {a} - {b} = {a - b}</p>
            <p>Умножение: {a} * {b} = {a * b}</p>
            <p>Деление: {a} / {b} = {a / b}</p>
            <p>Возведение в степень: {a}<sup>{b}</sup> = {a ** b}</p>''')

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_a(a):
    return redirect(f'/lab2/calc/{a}/1')


@app.route('/lab2/books')
def books():
    books = [
        {'author': 'Джек Лондон', 'title': 'Мартин Иден', 'genre': 'Роман', 'pages': 480},
        {'author': 'Этель Лилиан Войнич', 'title': 'Овод', 'genre': 'Роман', 'pages': 352},
        {'author': 'Сюзанна Кейсен', 'title': 'Прерванная дружба', 'genre': 'Мемуары', 'pages': 239},
        {'author': 'Мэри Рено', 'title': 'Схимник', 'genre': 'Исторический роман', 'pages': 432},
        {'author': 'Джордж Оруэлл', 'title': '1984', 'genre': 'Антиутопия', 'pages': 328},
        {'author': 'Рэй Брэдбери', 'title': '451 градус по Фаренгейту', 'genre': 'Антиутопия', 'pages': 176},
        {'author': 'Чарльз Диккенс', 'title': 'Большие надежды', 'genre': 'Роман', 'pages': 544},
        {'author': 'Диана Уинн Джонс', 'title': 'Ходячий замок', 'genre': 'Фэнтези', 'pages': 320},
        {'author': 'Джек Лондон', 'title': 'Белый клык', 'genre': 'Роман', 'pages': 256},
        {'author': 'Айн Рэнд', 'title': 'Атлант расправил плечи', 'genre': 'Философский роман', 'pages': 1168}
    ]
    return render_template('books.html', books=books)

@app.route('/lab2/cups')
def cups():
    cups = [
        {"image": "ch_paper.jpg", "name": "Чашка из листа бумаги", "description": "Керамическая чашка объемом 300 мл. Характерный дизайн под бумагу напоминает об учебных буднях."},
        {"image": "ch_waves.jpg", "name": "Волнообразная чашка", "description": "Керамическая чашка объемом 250 мл. Волнообразная форма прекрасно подходит для мест с высокой сейсмичностью. "},
        {"image": "ch_surprise.jpg", "name": "Чашка с сюрпризом", "description": "Керамическая  чашка объемом 300 мл. Фигурка внутри не заставит грустить о закончившемся чае."},
        {"image": "ch_fingers.jpg", "name": "Чашка пятюня", "description": "Керамическая  чашка объемом 300 мл. Может убежать."},
        {"image": "ch_rich.jpg", "name": "Чашка для светских бесед", "description": "Фарфоровая чашка с золотистым покрытием объемом 200 мл."},
        {"image": "ch_ordinary.jpg", "name": "Бюджетная чашка", "description": "Бумажный стаканчик объемом 100 мл. Имеет скрытые таланты."},
    ]
    return render_template('cups.html', cups=cups)