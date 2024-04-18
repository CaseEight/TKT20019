import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets

def user_id():
    return session.get("user_id", 0)

def is_admin():
    id = user_id()
    sql = text("SELECT isAdmin FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]
    #return render_template("invalid.html", error="Ei oikeutta toimintoon")