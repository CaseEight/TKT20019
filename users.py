from flask import Flask
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, dotenv_values
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from app import app
from db import db
import manager
import users
import os
import secrets

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)


def user_id():
    return session.get("user_id", 0)

def is_admin():
    id = user_id()
    if id != 0:
        sql = text("SELECT isAdmin FROM users WHERE id=:id")
        result = db.session.execute(sql, {"id":id})
        return result.fetchone()[0]
    else:
        return False
    
def new_user():
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
    try:
        isadmin = request.form["isadmin"]
    except:
        return render_template("invalid.html", message="Valitse käyttäjän tyyppi")
    sql = text("INSERT INTO users (username, password, isadmin) VALUES (:username, :password, :isAdmin)")
    db.session.execute(sql, {"username":username, "password":hash_value, "isAdmin":isadmin})
    db.session.commit()


def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]
