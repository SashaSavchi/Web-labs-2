from flask import Blueprint, redirect, render_template, request, url_for
from db import db
from db.models import initiative, users, Vote
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
rgz = Blueprint('rgz', __name__) 

@rgz.route('/rgz/')
def rgz_page(): 
    page = int(request.args.get("page", 1))
    per_page = 20
    initiatives = db.session.query(initiative) \
        .filter_by(is_public=True) \
        .order_by(initiative.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)
    user_votes = {
        vote.initiative_id: vote.value for vote in db.session.query(Vote).filter_by(user_id=current_user.id).all()
    }
    message = request.args.get('message', None)
    title = request.args.get('title')
    return render_template('rgz/rgz.html', initiatives=initiatives, message=message, user_votes=user_votes, title=title)


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

    return redirect('/rgz/?message=success_reg')


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
        return redirect('/rgz/?message=success_log')

    return render_template('rgz/login.html', error='Ошибка входа: логин и/или пароль неверны')


@rgz.route('/rgz/logout')
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
        is_public=is_public,
        published_at=datetime.utcnow() if is_public else None
    )
    db.session.add(new_initiative)
    db.session.commit()

    return redirect('/rgz/my_initiatives')


@rgz.route('/rgz/my_initiatives')
@login_required
def my_initiatives():
    user_initiatives = db.session.query(initiative).filter_by(user_id=current_user.id).all()
    published_initiatives = db.session.query(initiative).filter_by(user_id=current_user.id, is_public=True).all()  
    return render_template('rgz/my_initiatives.html', initiatives=user_initiatives, published_initiatives=published_initiatives)


@rgz.route('/rgz/edit/<int:initiative_id>', methods=['GET', 'POST'])
@login_required
def edit(initiative_id):
    initiative_obj = db.session.query(initiative).filter(initiative.id == initiative_id, initiative.user_id == current_user.id).first()

    if not initiative_obj:
        return redirect('/rgz/my_initiatives')

    if request.method == 'GET':
        return render_template('rgz/create_initiative.html', login=current_user.login, is_edit=True, initiative=initiative_obj)

    title = request.form.get('title')
    text = request.form.get('text')
    is_public = request.form.get('is_public', 'off') == 'on'

    if not title or not text:
        return render_template('rgz/create_initiative.html', error='Заполните все поля', login=current_user.login, is_edit=True, initiative=initiative_obj)

    initiative_obj.title = title
    initiative_obj.text = text


    if is_public and not initiative_obj.is_public:
        initiative_obj.published_at = datetime.utcnow()

    initiative_obj.is_public = is_public
    db.session.commit()

    return redirect('/rgz/my_initiatives')


@rgz.route('/rgz/delete/<int:initiative_id>', methods=['POST'])
@login_required
def delete(initiative_id):
    initiative_to_delete = db.session.query(initiative).filter(initiative.id == initiative_id).first()
    
    if initiative_to_delete:
        if current_user.is_admin or initiative_to_delete.user_id == current_user.id:
            db.session.query(Vote).filter(Vote.initiative_id == initiative_id).delete()

            db.session.delete(initiative_to_delete)
            db.session.commit()

    if current_user.is_admin:
        return redirect('/rgz/admin/initiative_management')
    return redirect('/rgz/my_initiatives')


@rgz.route('/rgz/delete_account', methods=['POST'])
@login_required
def delete_account():
    if not current_user.is_admin:
        user = db.session.query(users).filter_by(id=current_user.id).first()
        if user:
            initiatives_to_delete = db.session.query(initiative).filter(
                initiative.user_id == user.id
            ).all()
            for initiative_item in initiatives_to_delete:
                db.session.query(Vote).filter(Vote.initiative_id == initiative_item.id).delete()
                db.session.delete(initiative_item)
            
            db.session.query(Vote).filter(Vote.user_id == user.id).delete()

            db.session.delete(user)
            db.session.commit()
        
        logout_user()
        return redirect('/rgz/')
    
    user_id = request.form.get('user_id')
    user_to_delete = db.session.query(users).filter_by(id=user_id).first()
    
    if user_to_delete and user_to_delete.id != current_user.id:
        initiatives_to_delete = db.session.query(initiative).filter(
            initiative.user_id == user_to_delete.id
        ).all()
        for initiative_item in initiatives_to_delete:
            db.session.query(Vote).filter(Vote.initiative_id == initiative_item.id).delete()
            db.session.delete(initiative_item)
        
        db.session.query(Vote).filter(Vote.user_id == user_to_delete.id).delete()

        db.session.delete(user_to_delete)
        db.session.commit()
    
    return redirect('/rgz/admin/user_management')


@rgz.route('/rgz/admin/user_management')
@login_required
def user_management():
    if not current_user.is_admin: 
        return redirect('/rgz/')
    
    all_users = db.session.query(users).all()
    return render_template('rgz/user_management.html', users=all_users)


@rgz.route('/rgz/admin/initiative_management')
@login_required
def initiative_management():
    if not current_user.is_admin:  
        return redirect('/rgz/')

    all_initiatives = db.session.query(initiative).all()
    return render_template('rgz/initiative_management.html', initiatives=all_initiatives)


@rgz.route('/rgz/vote/<int:initiative_id>', methods=['POST'])
@login_required
def vote(initiative_id):
    initiative_obj = db.session.query(initiative).filter_by(id=initiative_id).first()

    vote_type = request.form.get('vote')
    vote_value = 1 if vote_type == 'up' else -1

    user_vote = db.session.query(Vote).filter_by(user_id=current_user.id, initiative_id=initiative_id).first()

    if user_vote:
        if user_vote.value == vote_value:
            return redirect(f'/rgz/?message=already_voted&title={initiative_obj.title}')
        elif user_vote.value != vote_value:
            initiative_obj.votes_count -= user_vote.value 
            user_vote.value = vote_value 
            initiative_obj.votes_count += vote_value 
    else:
        new_vote = Vote(user_id=current_user.id, initiative_id=initiative_id, value=vote_value)
        db.session.add(new_vote)
        initiative_obj.votes_count += vote_value

    db.session.commit()

    if initiative_obj.votes_count < -10:
        db.session.delete(initiative_obj)
        db.session.commit()

    return redirect('/rgz/')


