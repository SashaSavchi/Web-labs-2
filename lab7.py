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

# films = [
#     {
#         "title_ru": "Ходячий замок",
#         "title": "Howl no Ugoku Shiro",
#         "year": 2004,
#         "description": "Злая ведьма заточила 18-летнюю Софи в тело старухи. \
#             Девушка-бабушка бежит из города куда глаза глядят и встречает удивительный \
#             дом на ножках, где знакомится с могущественным волшебником Хаулом и демоном Кальцифером. \
#             Кальцифер должен служить Хаулу по договору, условия которого он не может разглашать. \
#             Девушка и демон решают помочь друг другу избавиться от злых чар."
#     },
#     {
#         "title_ru": "Джентльмены",
#         "title": "The Gentlemen",
#         "year": 2019,
#         "description": "Один ушлый американец ещё со студенческих лет \
#             приторговывал наркотиками, а теперь придумал схему нелегального \
#             обогащения с использованием поместий обедневшей английской \
#             аристократии и очень неплохо на этом разбогател. Другой \
#             пронырливый журналист приходит к Рэю, правой руке американца, \
#             и предлагает тому купить киносценарий, в котором подробно \
#             описаны преступления его босса при участии других представителей \
#             лондонского криминального мира — партнёра-еврея, китайской диаспоры, \
#             чернокожих спортсменов и даже русского олигарха."
#     },
#     {
#         "title_ru": "Шрэк",
#         "title": "Shrek",
#         "year": 2001,
#         "description": "Жил да был в сказочном государстве большой зеленый великан \
#         по имени Шрэк. Жил он в гордом одиночестве в лесу, на болоте, которое считал \
#         своим. Но однажды злобный коротышка — лорд Фаркуад, правитель волшебного \
#         королевства, безжалостно согнал на Шрэково болото всех сказочных обитателей. \
#         И беспечной жизни зеленого великана пришел конец. Но лорд Фаркуад пообещал\
#         вернуть Шрэку болото, если великан добудет ему прекрасную принцессу Фиону,\
#         которая томится в неприступной башне, охраняемой огнедышащим драконом."
#     },
#     {
#         "title_ru": "1+1",
#         "title": "Intouchables",
#         "year": 2011,
#         "description": "Пострадав в результате несчастного случая, \
#             богатый аристократ Филипп нанимает в помощники человека, \
#             который менее всего подходит для этой работы, – молодого \
#             жителя предместья Дрисса, только что освободившегося \
#             из тюрьмы. Несмотря на то, что Филипп прикован к \
#             инвалидному креслу, Дриссу удается привнести в \
#             размеренную жизнь аристократа дух приключений."
#     },
#     {
#         "title_ru": "Пираты Карибского моря",
#         "title": "Pirates of the Caribbean",
#         "year": 2006,
#         "description": "Вновь оказавшись в ирреальном мире, лихой \
#             капитан Джек Воробей неожиданно узнает, что является \
#             должником легендарного капитана «Летучего Голландца» Дэйви Джонса. \
#             Джек должен в кратчайшие сроки решить эту проблему, \
#             иначе ему грозит вечное проклятие и рабское существование \
#             после смерти. Вдобавок ко всему, срывается свадьба Уилла \
#             Тернера и Элизабет Суонн, которые вынуждены составить \
#             Джеку компанию в его злоключениях…"
#     },
# ]


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

    if film.get('title_ru') == '':
        return {'title_ru': 'Укажите русское название'}, 400
    if film.get('year') == '':
        return {'year': 'Укажите год'}, 400

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