from flask import Blueprint, redirect, render_template, request, session
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

lab8 = Blueprint('lab8',__name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=session.get('login'))


@lab8.route('/lab8/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if login_form == '':
        return render_template('lab8/register.html', 
                               error='Заполните имя пользователя')
    if password_form == '':
        return render_template('lab8/register.html', 
                               error='Заполните пароль')
    
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html', 
                               error='Такой пользователь уже существует')
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)
    return render_template('lab8/success_reg.html',login = login_form)


@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember', 'False') == 'True'

    if login_form == '':
        return render_template('lab8/login.html', 
                               error='Заполните имя пользователя')
    if password_form == '':
        return render_template('lab8/login.html', 
                               error='Заполните пароль')
    
    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            return render_template('lab8/success_log.html', login=login_form)
        
    return render_template('lab8/login.html',login = login_form, 
                           error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')



@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create_article.html', login=current_user.login, is_edit=False, article={})

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite', 'off') == 'on'
    is_public = request.form.get('is_public', 'off') == 'on'

    if not title or not article_text:
        return render_template(
            'lab8/create_article.html', 
            error='Заполните все поля', 
            login=current_user.login, 
            is_edit=False, 
            article={'title': title, 'article_text': article_text, 'is_favorite': is_favorite, 'is_public': is_public}
        )

    new_article = articles(login_id=current_user.id, title=title, article_text=article_text, is_favorite=is_favorite, is_public=is_public)  
    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/list')


@lab8.route('/lab8/list')
@login_required
def list():
    login_id = current_user.id
    article_list = db.session.query(articles).filter(articles.login_id == login_id).all()
    if not article_list:  
        return render_template('/lab8/articles.html', error='У вас пока нет статей', favorite_error=None)

    favorite_articles = [article for article in article_list if article.is_favorite]
    if not favorite_articles:
        return render_template('/lab8/articles.html', articles=article_list, favorite_error='У вас пока нет любимых статей.')

    return render_template('/lab8/articles.html', articles=article_list)



@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = db.session.query(articles).filter(articles.id == article_id, articles.login_id == current_user.id).first()

    if request.method == 'GET':
        return render_template('lab8/create_article.html', login=current_user.login, is_edit=True, article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite', 'off') == 'on'
    is_public = request.form.get('is_public', 'off') == 'on'

    if not title or not article_text:
        return render_template('lab8/create_article.html', error='Заполните все поля', login=current_user.login, is_edit=True, article=article)

    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public
    db.session.commit()

    return redirect('/lab8/list')


@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete(article_id):
    article = db.session.query(articles).filter(articles.id == article_id, articles.login_id == current_user.id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
    return redirect('/lab8/list')


@lab8.route('/lab8/favorite/<int:article_id>', methods=['POST'])
@login_required
def favorite(article_id):
    article = db.session.query(articles).filter_by(id=article_id).first()
    if article:
        article.is_favorite = not article.is_favorite
        db.session.commit()
    return redirect('/lab8/list')


@lab8.route('/lab8/public_articles', methods=['GET'])
def public_articles():
    public_articles = db.session.query(articles).filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=public_articles, login=current_user.login if current_user.is_authenticated else None)


@lab8.route('/lab8/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        login_id = current_user.id
        user_articles = db.session.query(articles).filter(
            articles.login_id == login_id,
            (articles.title.like(f'%{search_query}%')) |
            (articles.article_text.like(f'%{search_query}%'))
        ).all()

        public_articles = db.session.query(articles).filter(
            articles.is_public == True,
            (articles.title.like(f'%{search_query}%')) |
            (articles.article_text.like(f'%{search_query}%'))
        ).all()

        if not user_articles and not public_articles:
            return render_template('/lab8/search_done.html', error='Ничего не найдено')

        return render_template(
            '/lab8/search_done.html',
            user_articles=user_articles,
            public_articles=public_articles
        )

    return render_template('/lab8/search.html')
