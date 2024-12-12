from flask import Blueprint, jsonify, render_template, request, session, current_app 
from datetime import datetime

lab7 = Blueprint('lab7',__name__)

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')

films = [
    {
        "title_ru": "Ходячий замок",
        "title": "Howl no Ugoku Shiro",
        "year": 2004,
        "description": "Злая ведьма заточила 18-летнюю Софи в тело старухи. \
            Девушка-бабушка бежит из города куда глаза глядят и встречает удивительный \
            дом на ножках, где знакомится с могущественным волшебником Хаулом и демоном Кальцифером. \
            Кальцифер должен служить Хаулу по договору, условия которого он не может разглашать. \
            Девушка и демон решают помочь друг другу избавиться от злых чар."
    },
    {
        "title_ru": "Джентльмены",
        "title": "The Gentlemen",
        "year": 2019,
        "description": "Один ушлый американец ещё со студенческих лет \
            приторговывал наркотиками, а теперь придумал схему нелегального \
            обогащения с использованием поместий обедневшей английской \
            аристократии и очень неплохо на этом разбогател. Другой \
            пронырливый журналист приходит к Рэю, правой руке американца, \
            и предлагает тому купить киносценарий, в котором подробно \
            описаны преступления его босса при участии других представителей \
            лондонского криминального мира — партнёра-еврея, китайской диаспоры, \
            чернокожих спортсменов и даже русского олигарха."
    },
    {
        "title_ru": "Шрэк",
        "title": "Shrek",
        "year": 2001,
        "description": "Жил да был в сказочном государстве большой зеленый великан \
        по имени Шрэк. Жил он в гордом одиночестве в лесу, на болоте, которое считал \
        своим. Но однажды злобный коротышка — лорд Фаркуад, правитель волшебного \
        королевства, безжалостно согнал на Шрэково болото всех сказочных обитателей. \
        И беспечной жизни зеленого великана пришел конец. Но лорд Фаркуад пообещал\
        вернуть Шрэку болото, если великан добудет ему прекрасную принцессу Фиону,\
        которая томится в неприступной башне, охраняемой огнедышащим драконом."
    },
    {
        "title_ru": "1+1",
        "title": "Intouchables",
        "year": 2011,
        "description": "Пострадав в результате несчастного случая, \
            богатый аристократ Филипп нанимает в помощники человека, \
            который менее всего подходит для этой работы, – молодого \
            жителя предместья Дрисса, только что освободившегося \
            из тюрьмы. Несмотря на то, что Филипп прикован к \
            инвалидному креслу, Дриссу удается привнести в \
            размеренную жизнь аристократа дух приключений."
    },
    {
        "title_ru": "Пираты Карибского моря",
        "title": "Pirates of the Caribbean",
        "year": 2006,
        "description": "Вновь оказавшись в ирреальном мире, лихой \
            капитан Джек Воробей неожиданно узнает, что является \
            должником легендарного капитана «Летучего Голландца» Дэйви Джонса. \
            Джек должен в кратчайшие сроки решить эту проблему, \
            иначе ему грозит вечное проклятие и рабское существование \
            после смерти. Вдобавок ко всему, срывается свадьба Уилла \
            Тернера и Элизабет Суонн, которые вынуждены составить \
            Джеку компанию в его злоключениях…"
    },
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Film not found"}, 404
    return films[id]


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Film not found"}, 404
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Film not found"}, 404
    film = request.get_json()
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
    if film['title'] == '':
        film['title'] = film['title_ru']
    films[id] = film
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
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
    if film['title'] == '':
        film['title'] = film['title_ru']
    films.append(film)
    id = {'id': len(films) - 1}
    return id