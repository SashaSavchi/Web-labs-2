from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/lab9.html')

@lab9.route('/lab9/age/', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form['age']
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)

@lab9.route('/lab9/gender/', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form['gender']
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)

@lab9.route('/lab9/preference/', methods=['GET', 'POST'])
def preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        preference = request.form['preference']
        return redirect(url_for('lab9.preference_n', name=name, age=age, gender=gender, preference=preference))
    return render_template('lab9/preference.html', name=name)

@lab9.route('/lab9/preference_n/', methods=['GET', 'POST'])
def preference_n():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    if request.method == 'POST':
        preference_n = request.form['preference_n']
        return redirect(url_for('lab9.congratulation', name=name, age=age, gender=gender, preference=preference, preference_n=preference_n))
    return render_template('lab9/preference_n.html', name=name, preference=preference)

@lab9.route('/lab9/congratulation/')
def congratulation():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    preference_n = request.args.get('preference_n')

    message = ""
    image = ""

    if age < 18:
        message = f"Дорогой(ая) {name}, пусть этот Новый год принесет много радости и тепла."
        if gender == 'male':
            message += " Желаю тебе быстро вырасти и стать настоящим героем!"
        else:
            message += " Желаю тебе стать умной и прекрасной принцессой!"

        if preference == 'веселье':
            if preference_n == 'игрушки':
                message += " Лови в подарок игрушечного медвежонка!"
                image = 'toy_bear.jpg'
            elif preference_n == 'игры':
                message += " Лови настольную игру для всей семьи!"
                image = 'board_game.jpg'
        elif preference == 'сладости':
            if preference_n == 'конфеты':
                message += " Вот мешочек конфет для тебя!"
                image = 'candy_bag.jpg'
            elif preference_n == 'печенье':
                message += " Вот тебе коробка новогоднего печенья!"
                image = 'cookies.jpg'
    else:
        message = f"Поздравляю, {name}! Пусть Новый год будет наполнен счастьем и успехом."
        if gender == 'male':
            message += " Пусть каждый день будет продуктивным и радостным!"
        else:
            message += " Пусть каждый день будет наполнен улыбками и вдохновением!"

        if preference == 'подарки':
            if preference_n == 'технологии':
                message += " Вот тебе умный гаджет на праздник!"
                image = 'smart_gadget.jpg'
            elif preference_n == 'декор':
                message += " Вот красивый новогодний декор для дома!"
                image = 'home_decor.jpg'
        elif preference == 'еда':
            if preference_n == 'торт':
                message += " Вот праздничный торт для твоего стола!"
                image = 'cake.jpg'
            elif preference_n == 'шоколад':
                message += " Вот коробка элитного шоколада!"
                image = 'chocolate_box.jpg'

    return render_template('lab9/congratulation.html', message=message, image=image)