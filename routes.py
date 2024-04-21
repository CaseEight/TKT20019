from flask import Flask
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, dotenv_values
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from app import app
from db import db
import manager
import users
import secrets


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/new_user", methods=["POST"])
def new_user():
    users.new_user()
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["csrf_token"] = secrets.token_hex(16)
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("invalid.html", message="Väärä tunnus tai salasana")
    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/invalid")
def invalid():
    return render_template("invalid.html")

@app.route("/films")
def films():
    try:
        #sql = text("SELECT id, title, created_at FROM films ORDER BY id DESC")
        sql = text("SELECT F.id, title, CAST(AVG((rating)) AS Decimal (10,2)) AS average " \
            "FROM films F LEFT JOIN ratings R " \
            "ON F.id = R.films_id " \
            "GROUP By F.id, title " \
            "ORDER BY average DESC")
        result = db.session.execute(sql)
        films = result.fetchall()
        return render_template("films.html", films=films)
    except:
        return render_template("invalid.html", message="Ei näytettäviä elokuvia. Lisää elokuva yläreunan valikosta.")

@app.route("/new")
def new():
    if users.is_admin():
        return render_template("new.html")
    else:
        return render_template("/invalid.html", message="Ei oikeutta toimintoon")

@app.route("/create", methods=["POST"])
def create():
    title = request.form["title"]
    description = request.form["description"]
    length = request.form["length"]
    genre = request.form["genre"]
    director = request.form["director"]
    writer = request.form["writer"]
    sql = text("INSERT INTO films (title, description, length, genre, director, writer, created_at) VALUES (:title, :description, :length, :genre, :director, :writer, NOW()) RETURNING id")
    db.session.execute(sql, {"title":title, 
                            "description":description, 
                            "length":length, 
                            "genre":genre, 
                            "director":director, 
                            "writer":writer
                            })
    db.session.commit()
    sql = text("SELECT id FROM films WHERE title=:title")
    result = db.session.execute(sql, {"title":title})
    film_id = result.fetchone()[0]
    manager.all_visible_film_info(film_id)
    return redirect("/films")


@app.route("/delete", methods=["GET", "POST"])
def delete_film_route():
    if users.is_admin():
        flash("user_id", "error")
        if request.method == "GET":
            films = manager.get_film_list()
            return render_template("delete.html", list=films)
        if request.method == "POST":
            if "film" in request.form:
                film = request.form["film"]
                manager.delete_film(film)
            return redirect("/films")
    else:
        return render_template("/invalid.html", message="Ei oikeutta toimintoon")


@app.route("/delete_rating", methods=["POST"])
def delete_rating_route():
    if users.is_admin():
        rating_id = request.form["id"]
        film_id = manager.delete_rating(rating_id)
        return redirect("/result/" + str(film_id))
    else:
        return render_template("/invalid.html", message="Ei oikeutta toimintoon")

@app.route("/edit/<int:film_id>", methods=["GET", "POST"])
def edit_film_route(film_id):
    if request.method == "GET":
        film = manager.get_film(film_id) 
        return render_template("edit.html", film=film, film_id=film_id)
    elif request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        length = request.form.get("length")
        genre = request.form.get("genre")
        director = request.form.get("director")
        writer = request.form.get("writer")
        if manager.edit_film(film_id, title, description, length, genre, director, writer):
            return redirect(url_for('films')) 
        else:
            flash("Muokkaus epäonnistui.", "error")
            return redirect(url_for('edit_film', film_id=film_id))
    return render_template("films.html")

@app.route("/visible/<int:film_id>", methods=["GET", "POST"])
def visible(film_id):
    if users.is_admin():
        if request.method == "GET":
            film = manager.get_visible(film_id)
            return render_template("visible.html", film=film, film_id=film_id)
        elif request.method == "POST":
            title = request.form["title"]
            description = request.form["description"]
            length = request.form["length"]
            genre = request.form["genre"]
            director = request.form["director"]
            writer = request.form["writer"]
            manager.visible_film_update(film_id, title, description, length, genre, director, writer)
            return redirect("/films")
    else:
        return render_template("/invalid.html", message="Ei oikeutta toimintoon")



@app.route("/poll/<int:id>")
def poll(id):
    sql = text("SELECT title FROM films WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    title = result.fetchone()[0]
    return render_template("poll.html", id=id, title=title)

@app.route("/answer", methods=["POST"])
def answer():
    films_id = request.form["id"]
    if "answer" in request.form:
        rating = request.form["answer"]
        message = request.form["message"]
        sql2 = text("INSERT INTO ratings (films_id, rating, message, sent_at) VALUES (:films_id, :rating, :message, NOW())")
        db.session.execute(sql2, {"rating":rating, "films_id":films_id, "message":message})
        db.session.commit()
    return redirect("/result/" + str(films_id))

@app.route("/result/<int:id>")
def result(id):
    #leffan tiedot
    information = manager.get_film(id)
    #näytettävät tiedot
    visible = manager.get_visible(id)
    #keskiarvo
    sql = text("SELECT CAST(AVG((rating)) AS Decimal (10,2)) FROM ratings WHERE films_id=:films_id")
    result = db.session.execute(sql, {"films_id":id})
    average = result.fetchone()[0]
    #arvosanat ja kommentit
    sql = text("SELECT id, rating, message FROM ratings WHERE films_id=:films_id")
    result = db.session.execute(sql, {"films_id":id})
    ratings = result.fetchall()
    return render_template("result.html", visible=visible, average=average, ratings=ratings, information=information)


@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/searchresult", methods=["GET"])
def searchresult():
    query = request.args["query"]
    sql = text("SELECT * FROM films WHERE title ILIKE :query OR description ILIKE :query OR length ILIKE :query OR genre ILIKE :query OR director ILIKE :query OR writer ILIKE :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    films = result.fetchall()
    return render_template("searchresult.html", films=films)

