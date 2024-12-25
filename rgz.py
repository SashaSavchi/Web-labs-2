from flask import Blueprint, redirect, render_template, request, url_for
from db import db
from db.models import initiative, users
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

rgz = Blueprint('rgz', __name__) 

@rgz.route('/rgz/')
def rgz_page(): 
    page = int(request.args.get("page", 1))
    per_page = 20
    initiatives = db.session.query(initiative) \
        .filter_by(is_public=True) \
        .order_by(initiative.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)
    
    message = request.args.get('message', None)
    return render_template('rgz/rgz.html', initiatives=initiatives, message=message)


@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')

    login_form = request.form.get('login', '')
    password_form = request.form.get('password', '')

    if not login_form:
        return render_template('rgz/register.html', error='Заполните имя пользователя')

    if not password_form:
        return render_template('rgz/register.html', error='Заполните пароль')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('rgz/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('rgz.rgz_page', message='success_reg'))


@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login_form = request.form.get('login', '')
    password_form = request.form.get('password', '')
    remember = request.form.get('remember', 'False') == 'True'

    if not login_form:
        return render_template('rgz/login.html', error='Заполните имя пользователя')

    if not password_form:
        return render_template('rgz/login.html', error='Заполните пароль')

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember)
        return redirect(url_for('rgz.rgz_page', message='success_log'))

    return render_template('rgz/login.html', error='Ошибка входа: логин и/или пароль неверны')


@rgz.route('/rgz/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/rgz/')


@rgz.route('/rgz/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('rgz/create_initiative.html', login=current_user.login, is_edit=False, initiative={})

    title = request.form.get('title')
    text = request.form.get('text')
    is_public = request.form.get('is_public', 'off') == 'on'

    if not title or not text:
        return render_template(
            'rgz/create_initiative.html', 
            error='Заполните все поля', 
            login=current_user.login, 
            is_edit=False, 
            initiative={'title': title, 'text': text, 'is_public': is_public}
        )

    new_initiative = initiative(
        user_id=current_user.id, 
        title=title, 
        text=text, 
        is_public=is_public
    )
    db.session.add(new_initiative)
    db.session.commit()

    return redirect(url_for('rgz.rgz_page', message='initiative_created'))

@rgz.route('/rgz/my_initiatives')
@login_required
def my_initiatives():
    user_initiatives = db.session.query(initiative).filter_by(user_id=current_user.id).all()
    published_initiatives = db.session.query(initiative).filter_by(is_public=True).all()  
    return render_template('rgz/my_initiatives.html', initiatives=user_initiatives, published_initiatives=published_initiatives)

@rgz.route('/rgz/edit/<int:initiative_id>', methods=['GET', 'POST'])
@login_required
def edit(initiative_id):
    initiative_obj = db.session.query(initiative).filter(initiative.id == initiative_id, initiative.user_id == current_user.id).first()

    if not initiative_obj:
        return redirect(url_for('rgz.my_initiatives'))

    if request.method == 'GET':
        return render_template('rgz/create_initiative.html', login=current_user.login, is_edit=True, initiative=initiative_obj)

    title = request.form.get('title')
    text = request.form.get('text')
    is_public = request.form.get('is_public', 'off') == 'on'

    if not title or not text:
        return render_template('rgz/create_initiative.html', error='Заполните все поля', login=current_user.login, is_edit=True, initiative=initiative_obj)

    initiative_obj.title = title
    initiative_obj.text = text
    initiative_obj.is_public = is_public
    db.session.commit()

    return redirect(url_for('rgz.my_initiatives'))
