from flask import Flask
from flask import render_template, redirect, request, session
from os import getenv
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///"
db = SQLAlchemy(app)

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
        print("MOI")
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["password_verify"]
        email = request.form["email"]
        error = ""
        if password != verify :
            print("1")
            error = "Salasanat eivät ole samat"
        if len(password) < 6 :
            error = "Salasana liian lyhyt"
        hash_value = generate_password_hash(password)
        created = datetime.now()
        if error != "" :
            print("2")
            return render_template("signup.html", error=error)
        sql = "INSERT INTO users (username, password, email, created_on) VALUES (:username,:password,:email,:created_on)"  
        db.session.execute(sql, {"username": username, "password": hash_value, "email": email, "created_on": created})
        db.session.commit()
        print("3")
        return render_template("signup.html", success=True)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password, user_id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user == None :
        return render_template("login.html", error="Käyttäjä tai salasana väärin")
    else:
        print(user)
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["logged_in"] = True
            session["id"] = user[1]
            return redirect("/")
        else:
            return render_template("login.html", error="Käyttäjä tai salasana väärin")

@app.route("/logout", methods=["GET"])
def logout():
    session["logged_in"] = False
    session["id"] = ""
    return redirect("/")

@app.route("/moves")
def public_moves():
    sql = "SELECT * FROM moves WHERE public OR user_id=:id"
    result = db.session.execute(sql, {"id": session["id"]})
    moves = []
    for row in result:
        moves.append(row)
    return render_template("index.html", moves=moves)

@app.route("/move/<int:id>")
def move(id):
    sql = "SELECT * FROM moves WHERE move_id=:move_id AND (public OR user_id=:user_id)"
    result = db.session.execute(sql, {"move_id": id, "user_id": session["id"]})
    move = result.fetchone()
    if move == None:
        return render_template("404.html")
    print(move)
    return render_template("move.html", move=move)

@app.route("/newmove", methods=["GET", "POST"])
def newmove():
    if request.method == "GET":
        return render_template("newmove.html")
    else:
        name = request.form["name"]
        desc = request.form["desc"]
        if "public" not in request.form:
            public = "f"
        else:
            public = request.form["public"]
        if not session["logged_in"]:
            return redirect("/")
        sql = "INSERT INTO moves (name, description, public, user_id) VALUES (:name,:desc,:public,:user_id)"  
        db.session.execute(sql, {"name": name, "desc": desc, "public": public, "user_id": session["id"]})
        db.session.commit()
        return render_template("newmove.html", success=True)