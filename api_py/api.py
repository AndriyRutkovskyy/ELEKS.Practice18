from flask import (Flask, request, jsonify)
from db_mysql import Database

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/api/new/<ent>', methods=['POST'])
def create(ent):
    req_data = request.get_json()
    db = Database('localhost', 'root', 'root', 'py_api_db')
    resp = db.insert(ent, **req_data)

    result = '{} with id: {} was created!'.format(ent, resp)

    return result


@app.route('/api/schedule', methods=['GET'])
def schedule():
    join_query = 'film on film.id = schedule.movie_id '

    db = Database('localhost', 'root', 'root', 'py_api_db')
    resp = db.select('schedule', None, join_query, '*')
    d = []
    for row in resp:
        new_schedule = {
            "id": row['id'],
            "time": row['time'],
            "price": row['price'],
            "hall": row['hall_id'],
            "film": {"id": row['movie_id'], "name": row['name'], "genre": row['genre']}
        }

        d.append(new_schedule)

    return jsonify(d)


@app.route('/api/delete/<ent>/<id>', methods=['DELETE'])
def delete(ent, id):
    conditional_query = 'id = %s'

    db = Database('localhost', 'root', 'root', 'py_api_db')
    resp = db.delete(ent, conditional_query, id)

    if isinstance(resp, str):
        return resp
    elif isinstance(resp, int):
        if resp != 0:
            return '{} with id: {} was deleted!'.format(ent, id)
        else:
            return '{} with id: {} was not found!'.format(ent, id)


@app.route('/api/schedule/<genre>', methods=['PUT'])
def get_by_genre(genre):
    conditional_query = 'genre = %s'
    join_query = 'film on film.id = schedule.movie_id '

    db = Database('localhost', 'root', 'root', 'py_api_db')
    resp = db.select('schedule', conditional_query, join_query, 'time', 'name', 'genre', 'price', 'hall_id', genre=genre)

    return jsonify(resp)


@app.route('/api/film/<film_id>', methods=['PUT'])
def get_by_id(film_id):
    conditional_query = 'id = %s '

    db = Database('localhost', 'root', 'root', 'py_api_db')
    resp = db.select('film', conditional_query, None, 'id', 'name', 'genre', id=film_id)

    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='localhost', port=8081, debug=True)
