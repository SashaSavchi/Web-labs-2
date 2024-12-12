from flask import Blueprint, jsonify, render_template, request, session, current_app 
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7',__name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'alexandra_tsukanova_knowledge_base',
            user = 'alexandra_tsukanova_knowledge_base',
            password = '21581a'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films;")
    else:
        cur.execute("SELECT * FROM films;")

    films = cur.fetchall()
    db_close(conn, cur)
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?;", (id,))

    film = cur.fetchone()
    db_close(conn, cur)

    if film is None:
        return {"error": "Film not found"}, 404
    
    return film


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id = ?;", (id,))

    db_close(conn, cur)
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?;", (id,))
    
    film_in_db = cur.fetchone()

    if film_in_db is None:
        db_close(conn, cur)
        return {"error": "Film not found"}, 404

    film = request.get_json()

    if film['title'] == '' and film['title_ru'] == '':
        return {'title': 'Укажите оригинальное название'}, 400
    if film['title_ru'] == '':
        return {'title_ru': 'Укажите русское название'}, 400
    if film['year'] == '':
        return {'year': 'Укажите год'}, 400
    if film['title'] == '':
        film['title'] == film['title_ru']

    current_year = datetime.now().year
    year = int(film['year'])
    if year < 1895 or year > current_year:
        return {'year': f'Год должен быть от 1895 до {current_year}'}, 400
    
    if film.get('description') == '':
        return {'description': 'Заполните описание'}, 400

    if len(film.get('description', '')) > 2000:
        return {'description': 'Описание превышает 2000 символов'}, 400

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s;", 
                    (film['title'], film['title_ru'], film['year'], film['description'], id))
    else:
        cur.execute("UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?;", 
                    (film['title'], film['title_ru'], film['year'], film['description'], id))
    
    db_close(conn, cur)
    return film


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    conn, cur = db_connect()
    film = request.get_json()

    if film['title'] == '' and film['title_ru'] == '':
        return {'title': 'Укажите оригинальное название'}, 400
    if film['title_ru'] == '':
        return {'title_ru': 'Укажите русское название'}, 400
    if film['year'] == '':
        return {'year': 'Укажите год'}, 400
    if film['title'] == '':
        film['title'] == film['title_ru']
    
    current_year = datetime.now().year
    year = int(film['year'])
    if year < 1895 or year > current_year:
        return {'year': f'Год должен быть от 1895 до {current_year}'}, 400
    
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    description = film.get('description', '')
    
    if len(description) > 2000:
        return {'description': 'Описание превышает 2000 символов'}, 400
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id;", 
                    (film['title'], film['title_ru'], film['year'], film['description']))
    else:
        cur.execute("INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?);", 
                    (film['title'], film['title_ru'], film['year'], film['description']))
    film_id = cur.fetchone()['id']
    
    db_close(conn, cur)
    
    return {'id': film_id}