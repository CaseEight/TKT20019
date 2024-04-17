from flask import Flask
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, dotenv_values
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from app import app
from db import db
import manager
#import users


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/lisaa_kayttaja", methods=["POST"])
def lisaa_kayttaja():
    username = request.form["username"]
    if len(username) < 1:
        return render_template("invalid.html", message="Tunnuskenttä tyhjä")
    elif len(username) > 16:
        return render_template("invalid.html", message="Tunnuksessa voi olla korkeintaan 16 merkkiä")
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("invalid.html", message="Salasanat eroavat toisistaan")
    if password1 == "" or password2 == "":
        return render_template("invalid.html", message="Salasanakenttä on tyhjä")
    hash_value = generate_password_hash(password1)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return render_template("index.html")



@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return render_template("invalid.html", message="Väärä tunnus tai salasana")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user.id
            session["username"] = username
            return redirect("/")
        else:
            return redirect("/invalid")
    
@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/invalid")
def invalid():
    return render_template("invalid.html")


@app.route("/elokuvat")
def elokuvat():
    #sql = text("SELECT id, nimi, created_at FROM elokuvat ORDER BY id DESC")
    sql = text("SELECT E.id, nimi, CAST(AVG((rating)) AS Decimal (10,2)) AS average " \
        "FROM elokuvat E LEFT JOIN ratings R " \
        "ON E.id = R.elokuvat_id " \
        "GROUP By E.id, nimi " \
        "ORDER BY average DESC")
    result = db.session.execute(sql)
    elokuvat = result.fetchall()
    return render_template("elokuvat.html", elokuvat=elokuvat)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    nimi = request.form["nimi"]
    kuvaus = request.form["kuvaus"]
    kesto = request.form["kesto"]
    genre = request.form["genre"]
    ohjaaja = request.form["ohjaaja"]
    kasikirjoittaja = request.form["kasikirjoittaja"]
    sql = text("INSERT INTO elokuvat (nimi, kuvaus, kesto, genre, ohjaaja, kasikirjoittaja, created_at) VALUES (:nimi, :kuvaus, :kesto, :genre, :ohjaaja, :kasikirjoittaja, NOW()) RETURNING id")
    result = db.session.execute(sql, {"nimi":nimi, 
                                    "kuvaus":kuvaus, 
                                    "kesto":kesto, 
                                    "genre":genre, 
                                    "ohjaaja":ohjaaja, 
                                    "kasikirjoittaja":kasikirjoittaja
                                    })
    elokuvat_id = result.fetchone()[0]
    choices = request.form.getlist("choice")
    for choice in choices:
        if choice != "":
            sql = text("INSERT INTO choices (elokuvat_id, choice) VALUES (:elokuvat_id, :choice)")
            db.session.execute(sql, {"elokuvat_id":elokuvat_id, "choice":choice})
    db.session.commit()
    return redirect("/elokuvat")

@app.route("/delete", methods=["GET", "POST"])
def delete_film_route():
    #user_id = session.get("user_id")
    if request.method == "GET":
        films = manager.get_film_list()
        return render_template("delete.html", list=films)
    if request.method == "POST":
        if "film" in request.form:
            film = request.form["film"]
            manager.delete_film(film)
            #message = "Elokuva poistettu"
        #my_tasks = get_task_list(users.user_id())  #päivitetään tehtävälista/muistiinpanot
        return redirect("/elokuvat")  #lisätään viesti templateen
        #"return redirect("/") ??





@app.route("/poll/<int:id>")
def poll(id):
    sql = text("SELECT nimi FROM elokuvat WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    nimi = result.fetchone()[0]
    return render_template("poll.html", id=id, nimi=nimi)

@app.route("/answer", methods=["POST"])
def answer():
    elokuvat_id = request.form["id"]
    if "answer" in request.form:
        rating = request.form["answer"]
        message = request.form["message"]
        sql2 = text("INSERT INTO ratings (elokuvat_id, rating, message, sent_at) VALUES (:elokuvat_id, :rating, :message, NOW())")
        db.session.execute(sql2, {"rating":rating, "elokuvat_id":elokuvat_id, "message":message})
        db.session.commit()
    return redirect("/result/" + str(elokuvat_id))

@app.route("/result/<int:id>")
def result(id):
    #leffan tiedot
    sql = text("SELECT nimi, kuvaus, kesto, genre, ohjaaja, kasikirjoittaja FROM elokuvat WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    information = result.fetchone()
    #keskiarvo
    sql = text("SELECT CAST(AVG((rating)) AS Decimal (10,2)) FROM ratings WHERE elokuvat_id=:elokuvat_id")
    result = db.session.execute(sql, {"elokuvat_id":id})
    average = result.fetchone()[0]
    #arvosanat ja kommentit
    sql2 = text("SELECT rating, message FROM ratings WHERE elokuvat_id=:elokuvat_id")
    result = db.session.execute(sql2, {"elokuvat_id":id})
    ratings = result.fetchall()

    return render_template("result.html", nimi=information.nimi, kuvaus=information.kuvaus, kesto=information.kesto, genre=information.genre, ohjaaja=information.ohjaaja, kasikirjoittaja=information.kasikirjoittaja, average=average, ratings=ratings)


@app.route("/haku")
def haku():
    return render_template("haku.html")

@app.route("/hakutulos", methods=["GET"])
def hakutulos():
    query = request.args["query"]
    sql = text("SELECT * FROM elokuvat WHERE nimi ILIKE :query OR kuvaus ILIKE :query OR kesto ILIKE :query OR genre ILIKE :query OR ohjaaja ILIKE :query OR kasikirjoittaja ILIKE :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    elokuvat = result.fetchall()
    return render_template("hakutulos.html", elokuvat=elokuvat)

