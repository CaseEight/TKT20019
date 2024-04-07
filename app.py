from flask import Flask
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, dotenv_values
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    db.session.execute(text("INSERT INTO visitors (time) VALUES (NOW())"))
    db.session.commit()
    result = db.session.execute(text("SELECT COUNT(*) FROM visitors"))
    counter = result.fetchone()[0]
    return render_template("index.html", counter=counter) 