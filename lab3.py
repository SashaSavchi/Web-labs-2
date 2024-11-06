from flask import Blueprint, url_for, redirect, render_template, request, make_response
lab3 = Blueprint('lab3',__name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'Аноним')
    age = request.cookies.get('age', 'возраст неизвестен')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age = 5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta', max_age = 5)
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    resp.delete_cookie('bcolor')
    resp.delete_cookie('color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_family')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


price = 0 
@lab3.route('/lab3/pay')
def pay():
    global price
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
        
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    global price 
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    bcolor = request.args.get('bcolor')
    color = request.args.get('color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')

    resp = make_response(redirect('/lab3/settings'))

    if bcolor:
        resp.set_cookie('bcolor', bcolor)
    if color:
        resp.set_cookie('color', color)
    if font_size:
        resp.set_cookie('font_size', font_size)
    if font_family:
        resp.set_cookie('font_family', font_family)

    if bcolor or font_size or font_family or color:
        return resp

    return render_template('lab3/settings.html', bcolor=request.cookies.get('bcolor'), color=request.cookies.get('color'), font_size=request.cookies.get('font_size'), font_family=request.cookies.get('font_family'))


@lab3.route('/lab3/ticket_form')
def ticket_form():
    return render_template('lab3/ticket_form.html')


@lab3.route('/lab3/generate_ticket')
def generate_ticket():
    name = request.args.get('name')
    berth = request.args.get('berth')
    bed = 'bed' in request.args
    luggage = 'luggage' in request.args
    age = int(request.args.get('age', 0))
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = 'insurance' in request.args

    # Расчёт стоимости билета
    if age < 18:
        ticket_type = "Детский билет"
        price = 700
    else:
        ticket_type = "Взрослый билет"
        price = 1000

    # Доплаты в зависимости от выбранных опций
    if berth in ['lower', 'lower_side']:
        price += 100
    if bed:
        price += 75
    if luggage:
        price += 250
    if insurance:
        price += 150

    return render_template(
        '/lab3/ticket.html',
        name=name,
        berth=berth,
        age=age,
        luggage=luggage,
        bed=bed,
        departure=departure,
        destination=destination,
        date=date,
        insurance=insurance,
        ticket_type=ticket_type,
        total_price=price
    )


# Доп задание. Поиск товаров по заданному диапазону цен.
books = [
    {"name": "1984", "price": 500, "author": "Джордж Оруэлл", "genre": "Научная фантастика"},
    {"name": "Мастер и Маргарита", "price": 600, "author": "Михаил Булгаков", "genre": "Роман"},
    {"name": "Убить пересмешника", "price": 550, "author": "Харпер Ли", "genre": "Роман"},
    {"name": "Война и мир", "price": 700, "author": "Лев Толстой", "genre": "Роман"},
    {"name": "Гарри Поттер и философский камень", "price": 450, "author": "Дж.К. Роулинг", "genre": "Фэнтези"},
    {"name": "Над пропастью во ржи", "price": 400, "author": "Джером Д. Сэлинджер", "genre": "Роман"},
    {"name": "Анна Каренина", "price": 800, "author": "Лев Толстой", "genre": "Роман"},
    {"name": "Степной волк", "price": 500, "author": "Герман Гессе", "genre": "Роман"},
    {"name": "Однажды в Америке", "price": 300, "author": "Донат Филе", "genre": "Роман"},
    {"name": "Маленький принц", "price": 350, "author": "Антуан де Сент-Экзюпери", "genre": "Детская литература"},
    {"name": "Дело Тёмных Лесов", "price": 650, "author": "Мария Ладо", "genre": "Фэнтези"},
    {"name": "Идиот", "price": 700, "author": "Федор Достоевский", "genre": "Роман"},
    {"name": "Норвегия" , "price": 750, "author": "Стивен Кинг", "genre": "Ужасы"},
    {"name": "Сказки старого Вильнюса", "price": 380, "author": "Кирилл Нерсесов", "genre": "Сказки"},
    {"name": "Тихий Дон", "price": 680, "author": "Михаил Шолохов", "genre": "Роман"},
    {"name": "Зулейха открывает глаза", "price": 500, "author": "Гузель Яхина", "genre": "Роман"},
    {"name": "Лето в Польше" , "price": 420, "author": "Людмила Улицкая", "genre": "Роман"},
    {"name": "Собеседник", "price": 300, "author": "Лев Шестов", "genre": "Философия"},
    {"name": "Лотерейный билет", "price": 330, "author": "Кристиан Бобин", "genre": "Роман"},
    {"name": "Снегурочка", "price": 550, "author": "Александр Островский", "genre": "Драма"},
    {"name": "Десять негритят", "price": 630, "author": "Агата Кристи", "genre": "Криминал"},
    {"name": "Сто лет одиночества", "price": 720, "author": "Габриэль Гарсиа Маркес", "genre": "Роман"},
]

@lab3.route('/lab3/products')
def products():
    return render_template('lab3/search_form.html')


@lab3.route('/lab3/filter_products')
def filter_products():
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)

    filtered_books = [
        book for book in books 
        if (min_price is None or book['price'] >= min_price) and 
        (max_price is None or book['price'] <= max_price)
        ]
    
    return render_template('lab3/resultfiltr.html', books=filtered_books, min_price=min_price, max_price=max_price)
