from flask import Blueprint, render_template, request, redirect, url_for, session, flash

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    if all(key in session for key in ['name', 'age', 'gender', 'preference', 'preference_n']):
        return redirect(url_for('lab9.congratulation'))

    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name 
        return redirect(url_for('lab9.age'))
    
    return render_template('lab9/lab9.html')

@lab9.route('/lab9/age/', methods=['GET', 'POST'])
def age():
    if 'name' not in session:
        return redirect(url_for('lab9.lab'))

    name = session['name']
    
    if request.method == 'POST':
        age = request.form['age']
        session['age'] = age 
        return redirect(url_for('lab9.gender'))
    
    return render_template('lab9/age.html', name=name)

@lab9.route('/lab9/gender/', methods=['GET', 'POST'])
def gender():
    if 'name' not in session or 'age' not in session:
        return redirect(url_for('lab9.lab'))

    name = session['name']
    age = session['age']
    
    if request.method == 'POST':
        gender = request.form['gender']
        session['gender'] = gender  
        return redirect(url_for('lab9.preference'))
    
    return render_template('lab9/gender.html', name=name, age=age)

@lab9.route('/lab9/preference/', methods=['GET', 'POST'])
def preference():
    if 'name' not in session or 'age' not in session or 'gender' not in session:
        return redirect(url_for('lab9.lab'))

    name = session['name']
    age = session['age']
    gender = session['gender']
    
    if request.method == 'POST':
        preference = request.form['preference']
        session['preference'] = preference  
        return redirect(url_for('lab9.preference_n'))
    
    return render_template('lab9/preference.html', name=name, age=age, gender=gender)

@lab9.route('/lab9/preference_n/', methods=['GET', 'POST'])
def preference_n():
    if 'name' not in session or 'preference' not in session:
        return redirect(url_for('lab9.lab'))

    name = session['name']
    preference = session['preference']
    
    if request.method == 'POST':
        if 'preference_n' in request.form:
            preference_n = request.form['preference_n']
            session['preference_n'] = preference_n  
            return redirect(url_for('lab9.congratulation'))
        else:
            flash("Выберите один из вариантов.", "error")
        
    return render_template('lab9/preference_n.html', name=name, preference=preference)

@lab9.route('/lab9/congratulation/')
def congratulation():
    if not all(key in session for key in ['name', 'age', 'gender', 'preference', 'preference_n']):
        return redirect(url_for('lab9.lab'))

    name = session['name']
    age = int(session['age'])
    gender = session['gender']
    preference = session['preference']
    preference_n = session['preference_n']

    message = ""
    image = ""

    if age < 18:
        if gender == 'male':
            message = f"Дорогой {name}, пусть этот Новый год принесет много радости и тепла."
            message += " Желаю тебе быстро вырасти и стать настоящим героем!"
        else:
            message = f"Дорогая {name}, пусть этот Новый год принесет много радости и тепла."
            message += " Желаю тебе стать умной и прекрасной принцессой!"

        if preference == 'веселье':
            if preference_n == 'плюшевые игрушки':
                message += " Лови в подарок мягкого друга!"
                image = 'lab9/toy.jpg'
            elif preference_n == 'настольные игры':
                message += " Лови настольную игру!"
                image = 'lab9/board_game.jpg'
        elif preference == 'сладости':
            if preference_n == 'конфеты':
                message += " Вот тебе пиньята! БЕЙ!! "
                image = 'lab9/penyata.jpg'
            elif preference_n == 'печенье':
                message += " Вот тебе коробка новогоднего печенья!"
                image = 'lab9/cookies.jpg'
        elif preference == 'подарки':
            if preference_n == 'технологии':
                message += " Вот тебе приставка!"
                image = 'lab9/ps.jpg'
            elif preference_n == 'декор':
                message += " Вот тебе чудесные снеговики, которые подарят волшебство твоему дому!"
                image = 'lab9/snowman.jpg'
        elif preference == 'еда':
            if preference_n == 'торт':
                message += " Вот чудесный тортик для твоего стола!"
                image = 'lab9/cake.jpg'
            elif preference_n == 'шоколад':
                message += " Вот тебе огромный киндер!"
                image = 'lab9/ks.jpg'
    else:
        message = f"Поздравляю, {name}! Пусть Новый год будет наполнен счастьем и успехом."
        if gender == 'male':
            message += " Пусть каждый день будет продуктивным и радостным!"
        else:
            message += " Пусть каждый день будет наполнен улыбками и вдохновением!"

        if preference == 'веселье':
            if preference_n == 'плюшевые игрушки':
                message += " Лови в подарок мягкого друга!"
                image = 'lab9/toy.jpg'
            elif preference_n == 'настольные игры':
                message += " Лови настольную игру!"
                image = 'lab9/board_game.jpg'
        elif preference == 'сладости':
            if preference_n == 'конфеты':
                message += " Вот мешочек конфет для тебя!"
                image = 'lab9/candy.jpg'
            elif preference_n == 'печенье':
                message += " Вот тебе коробка новогоднего печенья!"
                image = 'lab9/cookies.jpg'
        elif preference == 'подарки':
            if preference_n == 'технологии':
                message += " Вот тебе практичный подарок!"
                image = 'lab9/comp.png'
            elif preference_n == 'декор':
                message += " Вот красивый новогодний декор для дома!"
                image = 'lab9/decor.jpg'
        elif preference == 'еда':
            if preference_n == 'торт':
                message += " Вот праздничный торт для твоего стола!"
                image = 'lab9/cake.jpg'
            elif preference_n == 'шоколад':
                message += " Вот коробка элитного шоколада!"
                image = 'lab9/choco.jpg'

    return render_template('lab9/congratulation.html', message=message, image=image)

@lab9.route('/lab9/reset/')
def reset():
    session.clear()
    return redirect(url_for('lab9.lab'))