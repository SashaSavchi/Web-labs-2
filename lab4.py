from flask import Blueprint, redirect, render_template, request, session
lab4 = Blueprint('lab4',__name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/calc/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/calc/div.html', error='Оба поля должны быть заполнены!')
    if x2 == '0':
        return render_template('lab4/calc/div.html', error='Делить на ноль нельзя!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/calc/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/calc/sum-form.html')


@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    if x1 == '':
        x1 = '0'
    if x2 == '':
        x2 = '0'
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/calc/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/calc/mult-form.html')


@lab4.route('/lab4/mult', methods = ['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = '1'
    if x2 == '':
        x2 = '1'
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/calc/mult.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/calc/sub-form.html')


@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/calc/sub.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/calc/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/st-form')
def st_form():
    return render_template('lab4/calc/st-form.html')


@lab4.route('/lab4/st', methods = ['POST'])
def st():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/calc/st.html', error='Оба поля должны быть заполнены!')
    if x1 == '0' and x2 == '0':
        return render_template('lab4/calc/st.html', error='Оба поля не должны равняться нулю одновременно')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/calc/st.html', x1=x1, x2=x2, result=result)


max_trees = 4
tree_count = 0
@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=max_trees)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < max_trees:
        tree_count += 1
    
    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Иванов', 'gender': 'мужской'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Смирнов', 'gender': 'мужской'},
    {'login': 'sam', 'password': '007', 'name': 'Саманта Цербер', 'gender': 'женский'},
    {'login': 'yan', 'password': '213', 'name': 'Яна Кузнецова', 'gender': 'женский'},
]


@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = session['name']
        else:
            authorized = False
            login = ''
            name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login)
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login)
    
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name'] 
            return redirect('/lab4/login')
        
    error = 'Неверный логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods = ['GET', 'POST'])
def fridge():
    message = ""
    snowflakes = 0  # Количество снежинок
    
    if request.method == 'POST':
        temperature = request.form.get('temperature', type = int)
        
        if temperature is None:
            message = "Ошибка: не задана температура"
        else:
            if temperature < -12:
                message = "Не удалось установить температуру — слишком низкое значение"
            elif temperature > -1:
                message = "Не удалось установить температуру — слишком высокое значение"
            elif -12 <= temperature <= -9:
                message = f"Установлена температура: {temperature}°С"
                snowflakes = 3
            elif -8 <= temperature <= -5:
                message = f"Установлена температура: {temperature}°С"
                snowflakes = 2
            elif -4 <= temperature <= -1:
                message = f"Установлена температура: {temperature}°С"
                snowflakes = 1

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)


@lab4.route('/lab4/order_grain', methods=['GET', 'POST'])
def order_grain():
    grain_prices = {
        'ячмень': 12345,
        'овёс': 8522,
        'пшеница': 8722,
        'рожь': 14111
    }

    message = ""
    discount_message = ""

    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight', type=float)

        # Проверка наличия типа зерна и валидности веса
        if weight is None:
            message = "Ошибка: не указан вес."
        elif weight <= 0:
            message = "Ошибка: вес должен быть больше 0."
        elif weight > 500:
            message = "Такого объёма сейчас нет в наличии."
        else:
            price_per_ton = grain_prices[grain_type]
            total_price = weight * price_per_ton

            if weight > 50:
                discount = 0.10
                discount_amount = total_price * discount
                total_price -= discount_amount
                discount_message = f"Применена скидка 10% за большой объём. Скидка составила: {discount_amount:.2f} руб."

            message = f"Заказ успешно сформирован. Вы заказали {grain_type}. Вес: {weight} т. Сумма к оплате: {total_price:.2f} руб."

    return render_template('lab4/order_grain.html', message=message, discount_message=discount_message, grain_prices=grain_prices)
