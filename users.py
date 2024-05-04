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
    del session["csrf_token"]
