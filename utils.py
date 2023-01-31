import sqlite3


def get_all(query):

    with sqlite3.connect("D:/PyCharm/DZ_14/netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = []

        for i in connection.execute(query).fetchall():
            result.append(dict(i))

        return result


def get_one(query):

    with sqlite3.connect("D:/PyCharm/DZ_14/netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchone()

        if result is None:
            return None
        else:
            return dict(result)


def get_by_genre(type_movie, release_year, listed_in):
    query = f"""
       SELECT title, description
       FROM netflix
       WHERE 'type' = '{type_movie}'
       AND release_year = '{release_year}'
       AND listed_in LIKE '%{listed_in}%'
       """

    result = []

    for i in get_all(query):
        result.append(
            {
                "title": i["title"],
                "description": i["description"]
            }
        )

    return result


def search_by_cast(name1, name2):
    query = f"""
           SELECT *
           FROM netflix
           WHERE netflix."cast" LIKE '%Jack Black%' 
           AND netflix."cast" LIKE '%Dustin Hoffman%'
           """

    cast = []
    set_cast = set()
    result = get_all(query)

    for i in result:
        for actor in i['cast'].split(','):
            cast.append(actor)

    for actor in cast:
        if cast.count(actor) > 2:
            set_cast.add(actor)

    return list(set_cast)
