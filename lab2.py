from flask import Blueprint, url_for, redirect, render_template, request
lab2 = Blueprint('lab2',__name__)


@lab2.route('/lab2/a/')
def a():
    return render_template("base.html", 
                           lab='Лабораторная работа 2', 
                           main_content='со слэшем')


@lab2.route('/lab2/a')
def a2():
    return render_template("base.html", 
                           lab='Лабораторная работа 2', 
                           main_content='без слэша')


@lab2.route('/lab2/')
def lab21():
    return render_template('lab2.html')


flower_list = [
    {'name': 'Роза', 'price': 150},
    {'name': 'Тюльпан', 'price': 80},
    {'name': 'Незабудка', 'price': 100},
    {'name': 'Ромашка', 'price': 50}
]
# поправить
@lab2.route('/lab2/flowers/<int:flower_id>')
def flower(flower_id):
    if flower_id >= len(flower_list):
        return render_template("base.html", 
                            lab='Лабораторная работа 2', 
                            main_content='такого цветка нет'), 404 
    else:
        flower = flower_list[flower_id]
        return render_template("base.html",
                               lab='Лабораторная работа 2',
                               main_content=f'''
                                   <h1>Цветок: {flower["name"]}</h1>
                                   <p>Цена: {flower["price"]}&#x20bd;</p>
                                   <a href="/lab2/all_flowers">Все цветы</a>
                               ''')
# @lab2.route('/lab2/add_flower/', defaults={'name': ''})
# # запрос по адресу /lab2/add_flower/ ожидал, что после /add_flower/ 
# # будет следовать значение для параметра <name>. Тк это значение отсутствовало, возникал ответ 404.
# @lab2.route('/lab2/add_flower/<name>')
# def add_flower(name):
#     if name == '':
#         return render_template("base.html", 
#                     lab='Лабораторная работа 2', 
#                     main_content='Вы не задали имя цветка'), 400
#     elif name not in flower_list:
#         flower_list.lab2end(name)
#         return render_template("base.html", 
#                     lab='Лабораторная работа 2', 
#                     main_content=f'''
#             <h1>Добавлен новый цветок</h1>
#             <p>Название нового цветка: {name} </p>
#             <p>Всего цветов: {len(flower_list)}</p>
#             <p>Полный список: {flower_list}</p>''')
#     else:
#         return render_template("base.html", 
#                     lab='Лабораторная работа 2', 
#                     main_content=f'''
#             <h1>Такой цветок уже есть в списке.</h1>
#             <a href="/lab2/all_flowers">Полный список</a>'''), 400


# из доп задания
@lab2.route('/lab2/all_flowers')
def all_flowers():
    message = request.args.get('message')  # Получаем сообщение из параметров URL
    flowers_html = '<ol>'
    for index, flower in enumerate(flower_list):
        flowers_html += f'''<li>{flower["name"]} - {flower["price"]}&#x20bd; 
        <a href="/lab2/del_flower/{index}">Удалить</a></li>'''
    flowers_html += '</ol>'
    add_flower_form = '''
        <form action="/lab2/add_flower" method="post">
            <input type="text" name="flower_name" placeholder="Имя цветка" required>
            <input type="number" min="0" name="flower_price" placeholder="Цена цветка" required>
            <button type="submit">Добавить</button>
        </form>
    '''
    return render_template("base.html", 
                    lab='Лабораторная работа 2', 
                    main_content=f'''
            <h1>Все цветы</h1>
            {flowers_html}
            <p>Всего цветов: {len(flower_list)}</p>
            <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>
            <h2>Добавить новый цветок</h2>
            {add_flower_form}
            {'<p style="color: red;">' + message + '</p>' if message else ''}
            ''')


@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    flower_name = request.form['flower_name']
    flower_price = request.form['flower_price']
    if any(flower['name'] == flower_name for flower in flower_list):
        return redirect('/lab2/all_flowers?message=Такой%20цветок%20уже%20есть%20в%20списке.')
    else:
        flower_list.append({"name": flower_name, "price": flower_price})
        return redirect('/lab2/all_flowers')


@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id >= len(flower_list):
        return "Цветка с таким номером нет", 404
    else:
        del flower_list[flower_id]  # del Удаляем цветок по индексу
        return redirect('/lab2/all_flowers')


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return render_template("base.html", 
                    lab='Лабораторная работа 2', 
                    main_content='''<h1>Список цветов очищен</h1>
        <a href="/lab2/all_flowers">Все цветы</a>''')


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', phrase = phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_a(a):
    return redirect(f'/lab2/calc/{a}/1')


@lab2.route('/lab2/books')
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


@lab2.route('/lab2/cups')
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