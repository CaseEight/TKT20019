from db import db
from sqlalchemy.sql import text
#import users

def get_film_list():
    sql = text("SELECT id, title, description FROM films ORDER BY title DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def get_film(film_id):
    sql = text("SELECT * FROM films WHERE id=:film_id")
    result = db.session.execute(sql, {"film_id": film_id})
    film = result.fetchone()
    return film

def delete_film(film_id):
    sql = text("DELETE FROM films WHERE id=:film_id")
    db.session.execute(sql, {"film_id":film_id})
    db.session.commit()

def delete_rating(rating_id):
    sql = text("SELECT films_id FROM ratings WHERE id=:rating_id")
    result = db.session.execute(sql, {"rating_id":rating_id})
    film_id = result.fetchone()[0]
    sql = text("DELETE FROM ratings WHERE id=:rating_id")
    db.session.execute(sql, {"rating_id":rating_id})
    db.session.commit()
    return film_id

def edit_film(film_id, title, description, length, genre, director, writer):
    try:
        sql = text("UPDATE films SET title = COALESCE(:title, title), description = COALESCE(:description, description), " \
                "length = COALESCE(:length, length), genre = COALESCE(:genre, genre), " \
                "director = COALESCE(:director, director),writer = COALESCE(:writer, writer) " \
                    "WHERE id = :film_id")
        db.session.execute(sql, {"film_id":film_id,
                                "title":title, 
                                "description":description, 
                                "length":length, 
                                "genre":genre, 
                                "director":director, 
                                "writer":writer
                                })
        db.session.commit()
        return True
    except:
        return False
    
def all_visible_film_info(film_id):
    truth = text("True")
    sql = text("INSERT INTO film_visible (titleVisible, descriptionVisible, lengthVisible, genreVisible, directorVisible, writerVisible, created_atVisible, films_id) VALUES (TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, :films_id) RETURNING id")
    db.session.execute(sql, {"titleVisible":truth, "descriptionVisible":truth, "lengthVisible":truth, "genreVisible":truth, "directorVisible":truth, "writerVisible":truth, "created_atVisible":truth, "films_id":film_id})
    db.session.commit()

def get_visible(film_id):
    sql = text("SELECT * FROM film_visible WHERE films_id=:film_id")
    result = db.session.execute(sql, {"film_id": film_id})
    film = result.fetchone()
    return film


def visible_film_update(film_id, title, description, length, genre, director, writer):
    sql = text("UPDATE film_visible SET titleVisible = :title, descriptionVisible = :description, " \
            "lengthVisible = :length, genreVisible = :genre, " \
            "directorVisible = :director, writerVisible = :writer " \
            "FROM films WHERE films.id = film_visible.films_id "
                "AND films.id = :film_id")
    db.session.execute(sql, {"film_id":film_id,
                            "title":title, 
                            "description":description, 
                            "length":length, 
                            "genre":genre, 
                            "director":director, 
                            "writer":writer
                            })
    db.session.commit()