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
    resp.set_cookie('name_color', 'magenta')
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