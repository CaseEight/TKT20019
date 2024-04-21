from db import db
from sqlalchemy.sql import text
#import users

def get_film_list():
    sql = text("SELECT id, nimi, kuvaus FROM elokuvat ORDER BY nimi DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def get_film(film_id):
    sql = text("SELECT * FROM elokuvat WHERE id=:film_id")
    result = db.session.execute(sql, {"film_id": film_id})
    film = result.fetchone()
    return film

def delete_film(elokuva_id):
    sql = text("DELETE FROM elokuvat WHERE id=:elokuva_id")
    db.session.execute(sql, {"elokuva_id":elokuva_id})
    db.session.commit()

def delete_rating(rating_id):
    sql = text("SELECT elokuvat_id FROM ratings WHERE id=:rating_id")
    result = db.session.execute(sql, {"rating_id":rating_id})
    elokuva_id = result.fetchone()[0]
    sql = text("DELETE FROM ratings WHERE id=:rating_id")
    db.session.execute(sql, {"rating_id":rating_id})
    db.session.commit()
    return elokuva_id

def edit_film(elokuva_id, nimi, kuvaus, kesto, genre, ohjaaja, kasikirjoittaja):
    try:
        sql = text("UPDATE elokuvat SET nimi = COALESCE(:nimi, nimi), kuvaus = COALESCE(:kuvaus, kuvaus), " \
                "kesto = COALESCE(:kesto, kesto), genre = COALESCE(:genre, genre), " \
                "ohjaaja = COALESCE(:ohjaaja, ohjaaja),kasikirjoittaja = COALESCE(:kasikirjoittaja, kasikirjoittaja) " \
                    "WHERE id = :elokuva_id")
        db.session.execute(sql, {"elokuva_id":elokuva_id,
                                "nimi":nimi, 
                                "kuvaus":kuvaus, 
                                "kesto":kesto, 
                                "genre":genre, 
                                "ohjaaja":ohjaaja, 
                                "kasikirjoittaja":kasikirjoittaja
                                })
        db.session.commit()
        return True
    except:
        return False
    
def all_visible_film_info(film_id):
    truth = text("True")
    sql = text("INSERT INTO film_visible (nimiVisible, kuvausVisible, kestoVisible, genreVisible, ohjaajaVisible, kasikirjoittajaVisible, created_atVisible, elokuvat_id) VALUES (TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, :elokuvat_id) RETURNING id")
    db.session.execute(sql, {"nimiVisible":truth, "kuvausVisible":truth, "kestoVisible":truth, "genreVisible":truth, "ohjaajaVisible":truth, "kasikirjoittajaVisible":truth, "created_atVisible":truth, "elokuvat_id":film_id})
    db.session.commit()

def get_visible(film_id):
    sql = text("SELECT * FROM film_visible WHERE elokuvat_id=:film_id")
    result = db.session.execute(sql, {"film_id": film_id})
    film = result.fetchone()
    return film


def visible_film_update(film_id, nimi, kuvaus, kesto, genre, ohjaaja, kasikirjoittaja):
    sql = text("UPDATE film_visible SET nimiVisible = :nimi, kuvausVisible = :kuvaus, " \
            "kestoVisible = :kesto, genreVisible = :genre, " \
            "ohjaajaVisible = :ohjaaja, kasikirjoittajaVisible = :kasikirjoittaja " \
            "FROM elokuvat WHERE elokuvat.id = film_visible.elokuvat_id "
                "AND elokuvat.id = :film_id")
    db.session.execute(sql, {"film_id":film_id,
                            "nimi":nimi, 
                            "kuvaus":kuvaus, 
                            "kesto":kesto, 
                            "genre":genre, 
                            "ohjaaja":ohjaaja, 
                            "kasikirjoittaja":kasikirjoittaja
                            })
    db.session.commit()