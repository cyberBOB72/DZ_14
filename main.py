from flask import Flask, jsonify
from utils import get_all, get_one


app = Flask(__name__)

@app.get('/movie/<title>')
def get_by_title(title):
    query = f"""
    SELECT *
    FROM netflix
    WHERE title = '{title}'
    ORDER BY date_added DESC
    """

    q_result = get_one(query)

    if q_result is None:
        return jsonify(status=404)

    movie = {
        "title": q_result["title"],
        "country": q_result["country"],
        "release_year": q_result["release_year"],
        "genre": q_result["listed_in"],
        "description": q_result["description"]
    }

    return jsonify(movie)


@app.get('/movie/<year1>/to/<year2>')
def get_movie_by_year(year1, year2):
    query = f"""
    SELECT *
    FROM netflix
    WHERE release_year BETWEEN {year1} and {year2}
    LIMIT 100 
    """

    result = []

    for i in get_all(query):
        result.append(
            {
            "title": i["title"],
            "release_year": i["release_year"]
            }
        )

    return jsonify(result)


@app.get('/movie/rating/<id>')
def get_movie_by_rating(id):
    query = f"""
    SELECT *
    FROM netflix
    """

    if id == 'children':
        query += 'WHERE rating = "G"'
    elif id == 'family':
        query += 'WHERE rating = "G" or rating = "PG" or rating = "PG-13"'
    elif id == 'adult':
        query += 'WHERE rating = "R" or rating = "NC-17"'
    else:
        return jsonify(status=400)

    result = []

    for i in get_all(query):
        result.append(
            {
            "title": i["title"],
            "rating": i["rating"],
            "description": i["description"]
            }
        )

    return jsonify(result)


@app.get('/genre/<genre>')
def get_movie_by_genre(genre):
    query = f"""
    SELECT *
    FROM netflix
    WHERE listed_in LIKE '%{genre}%'
    ORDER BY date_added DESC
    LIMIT 10
    """

    result = []

    for i in get_all(query):
        result.append(
            {
            "title": i["title"],
            "description": i["description"]
            }
        )

    return jsonify(result)

app.run()
