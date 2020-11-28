from flask import Flask
from flask import render_template, redirect, request, session
from os import getenv
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

from db import db
import user
import moves

@app.route("/")
def index():
    if session.get("logged_in") :
        return render_template("index.html")
    else :
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET" :
        return render_template("signup.html", error="")
    else :
        rf = request.form
        created_user = user.create_new(rf["username"], rf["password"], rf["password_verify"], rf["email"])
        return render_template("signup.html", message=created_user)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    res = user.login(username, password)
    if res == "":
        return redirect("/")
    return render_template("login.html", error=res)

@app.route("/logout", methods=["GET"])
def logout():
    session["logged_in"] = False
    session["id"] = ""
    return redirect("/")

@app.route("/moves")
def public_moves():
    if not user.is_logged_in(): 
        return redirect("/")
    return render_template("index.html", moves=moves.get_all())

@app.route("/move/<int:move_id>")
def move(move_id):
    move = moves.get_one(move_id)
    if move == None:
        return render_template("404.html")
    return render_template("move.html", move=move)

@app.route("/newmove", methods=["GET", "POST"])
def newmove():
    if not user.is_logged_in():
        return redirect("/")
    if request.method == "GET":
        return render_template("newmove.html", admin=user.is_admin())
    else:
        name = request.form["name"]
        desc = request.form["desc"]
        public = "f"
        if "public" in request.form:
            public = request.form["public"]
        res = moves.create_new(name, desc, public)
        return render_template("newmove.html", message=res)

@app.route("/editmove/<int:move_id>", methods=["GET", "POST"])
def edit_move(move_id):
    if not user.is_logged_in():
        return redirect("/")
    if request.method == "GET":
        return render_template("edit_move.html", move=moves.get_one(move_id), admin=user.is_admin())
    else:
        name = request.form["name"]
        desc = request.form["desc"]
        public = "f"
        if "public" in request.form:
            public = request.form["public"]
        res = moves.edit_one(move_id, name, desc, public)
        return redirect("/move/"+str(move_id))