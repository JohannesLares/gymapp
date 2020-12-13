from db import db
from app import app
from os import urandom
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
import re

def is_admin():
    sql = "SELECT admin FROM users WHERE user_id=:id"
    result = db.session.execute(sql, {"id": get_id()})
    user = result.fetchone()
    return user[0]

def create_new(username, password, verify, email):
    error = ""
    if password != verify:
        error = "salasanat eivät ole samat. "
    if len(password) < 6:
        error = "salasana liian lyhyt. "
    if len(username) < 3:
        error = "Käyttäjätunnus liian lyhyt. "
    if not re.match("^[0-9a-öA-Ö_-]*$", username):
        error = "Käyttäjätunnuksessa pitää olla vain kirjaimia ja numeroita. "
    if len(email) < 6:
        error = "Sähköposti liian lyhyt. "
    hash_value = generate_password_hash(password)
    if error != "":
        return error
    sql = "INSERT INTO users (username, password, email, created_on) VALUES (:username,:password,:email,NOW())"  
    db.session.execute(sql, {"username": username, "password": hash_value, "email": email})
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Käyttäjätunnus tai sähköpostiosoite on jo käytössä"
    return "Rekisteröinti onnistui"

def login(username, password): 
    sql = "SELECT password, user_id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user == None:
        return "Käyttäjä tai salasana väärin"
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            sql = "UPDATE users SET last_login=NOW() WHERE user_id=:id"
            result = db.session.execute(sql, {"id": user[1]})
            db.session.commit()
            session["logged_in"] = True
            session["id"] = user[1]
            session["csrf"] = urandom(16).hex()
            return ""
        else:
            return "Käyttäjä tai salasana väärin"

def is_logged_in():
    if session.get("logged_in"):
        return session["logged_in"]
    return False

def get_id():
    if session.get("id"):
        return session["id"]
    return None

def check_csrf(token):
    if session.get("csrf"):
        if token == session.get("csrf"):
            return True
    return False