from db import db
from sqlalchemy.sql import text
#import users

def get_film_list():
    sql = text("SELECT id, nimi, kuvaus FROM elokuvat ORDER BY nimi DESC")
    result = db.session.execute(sql)
    return result.fetchall()


def delete_film(elokuva_id):
    sql = text("DELETE FROM elokuvat WHERE id=:elokuva_id")
    db.session.execute(sql, {"elokuva_id":elokuva_id})
    db.session.commit()

