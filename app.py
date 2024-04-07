from flask import Flask
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, dotenv_values
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/lisaa_kayttaja", methods=["POST"])
def lisaa_kayttaja():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
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
        return redirect("/invalid")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            return redirect("/invalid")
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/invalid")
def invalid():
    return render_template("invalid.html")


@app.route("/elokuvat")
def elokuvat():
    sql = text("SELECT id, nimi, created_at FROM elokuvat ORDER BY id DESC")
    result = db.session.execute(sql)
    elokuvat = result.fetchall()
    return render_template("elokuvat.html", elokuvat=elokuvat)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    nimi = request.form["nimi"]
    sql = text("INSERT INTO elokuvat (nimi, created_at) VALUES (:nimi, NOW()) RETURNING id")
    result = db.session.execute(sql, {"nimi":nimi})
    elokuvat_id = result.fetchone()[0]
    choices = request.form.getlist("choice")
    for choice in choices:
        if choice != "":
            sql = text("INSERT INTO choices (elokuvat_id, choice) VALUES (:elokuvat_id, :choice)")
            db.session.execute(sql, {"elokuvat_id":elokuvat_id, "choice":choice})
    db.session.commit()
    return redirect("/elokuvat")

@app.route("/poll/<int:id>")
def poll(id):
    sql = text("SELECT nimi FROM elokuvat WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    nimi = result.fetchone()[0]
    sql = text("SELECT id, choice FROM choices WHERE elokuvat_id=:id")
    result = db.session.execute(sql, {"id":id})
    choices = result.fetchall()
    return render_template("poll.html", id=id, nimi=nimi, choices=choices)

@app.route("/answer", methods=["POST"])
def answer():
    elokuvat_id = request.form["id"]
    if "answer" in request.form:
        choice_id = request.form["answer"]
        sql = text("INSERT INTO answers (choice_id, sent_at) VALUES (:choice_id, NOW())")
        db.session.execute(sql, {"choice_id":choice_id})
        db.session.commit()
    return redirect("/result/" + str(elokuvat_id))

@app.route("/result/<int:id>")
def result(id):
    sql = text("SELECT nimi FROM elokuvat WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    nimi = result.fetchone()[0]
    sql = text("SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN answers a " \
          "ON c.id=a.choice_id WHERE c.elokuvat_id=:elokuvat_id GROUP BY c.id")
    result = db.session.execute(sql, {"elokuvat_id":id})
    choices = result.fetchall()
    return render_template("result.html", nimi=nimi, choices=choices)

@app.route("/result", methods=["GET"])
def haku():
    query = request.args["query"]
    sql = text("SELECT id, content FROM elokuvat WHERE content LIKE :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    elokuvat = result.fetchall()
    return render_template("result.html", elokuvat=elokuvat)
