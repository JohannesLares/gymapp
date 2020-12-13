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
import plans
import training

# --- ROUTES ---

@app.route("/")
def index():
    if session.get("logged_in") :
        return render_template("index.html", noplans=True)
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
        return redirect("/403")
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
        return redirect("/403")
    if request.method == "GET":
        return render_template("newmove.html", admin=user.is_admin())
    else:
        if not user.check_csrf(request.form["csrf"]):
            return redirect("/400")
        name = request.form["name"]
        desc = request.form["desc"]
        public = "f"
        if "public" in request.form:
            public = request.form["public"]
        res = moves.create_new(name, desc, public)
        return render_template("newmove.html", message=res, admin=user.is_admin())

@app.route("/editmove/<int:move_id>", methods=["GET", "POST"])
def edit_move(move_id):
    if not user.is_logged_in():
        return redirect("/403")
    if request.method == "GET":
        return render_template("edit_move.html", move=moves.get_one(move_id), admin=user.is_admin())
    else:
        if not user.check_csrf(request.form["csrf"]):
            return redirect("/400")
        name = request.form["name"]
        desc = request.form["desc"]
        public = "f"
        if "public" in request.form:
            public = request.form["public"]
        res = moves.edit_one(move_id, name, desc, public)
        return redirect("/move/"+str(move_id))

@app.route("/deletemove", methods=["POST"])
def delete_move():
    if not user.is_logged_in():
        return redirect("/403")
    if not user.check_csrf(request.form["csrf"]):
        return redirect("/400")
    res = moves.delete_one(request.form["move_id"])
    if not res:
        return redirect("/400")
    return redirect("/moves")

@app.route("/plans")
def get_plans():
    if not user.is_logged_in():
        return redirect("/403")
    return render_template("plans.html", plans=plans.get_all())

@app.route("/plan/<int:plan_id>")
def get_plan(plan_id):
    if not user.is_logged_in():
        return redirect("/403")
    return render_template("plan.html", info=plans.get_info(plan_id), sets=plans.get_one(plan_id))

@app.route("/newplan", methods=["GET", "POST"])
def new_plan():
    if not user.is_logged_in():
        return redirect("/403")
    if request.method == "GET":
        return render_template("newplan.html")
    else:
        if not user.check_csrf(request.form["csrf"]):
            return redirect("/400")
        if float(request.form["amount"]) < 1:
            return render_template("newplan.html", error="Liikesarjoja oltava vähintään 1")
        res = plans.create_new_plan(request.form["name"], request.form["desc"])
        if isinstance(res, str):
            return render_template("newplan.html", error=res)
        return redirect("/newplan/"+str(res)+"/"+str(request.form["amount"]))

@app.route("/newplan/<int:plan_id>/<int:move_count>", methods=["GET", "POST"])
def add_moves_to_plan(plan_id, move_count):
    if not user.is_logged_in():
        return redirect("/403")
    if request.method == "GET":
        return render_template("editsetsonplan.html", plan_id=plan_id, count=move_count, moves=moves.get_all())
    else:
        if not user.check_csrf(request.form["csrf"]):
            return redirect("/400")
        plans.add_sets_to_new_plan(request.form, move_count, plan_id)
        return redirect("/plan/"+str(plan_id))

@app.route("/deletefromplan", methods=["POST"])
def delete_set_from_plan():
    if not user.is_logged_in():
        return "Fail", 403
    if not user.check_csrf(request.form["csrf"]):
        return "Fail", 400
    if plans.delete_set(request.form["set_id"]):
        return "Success", 200
    return "Fail", 400

@app.route("/editplacing", methods=["POST"])
def edit_set_placing_on_plan():
    if not user.is_logged_in():
        return "Fail", 403
    if not user.check_csrf(request.form["csrf"]):
        return "Fail", 400
    if plans.move_set(request.form["set_id"], request.form["new_position"]):
        return "Success", 200
    return "Error", 500

@app.route("/deleteplan", methods=["POST"])
def delete_plan():
    if not user.is_logged_in():
        return "Fail", 403
    if not user.check_csrf(request.form["csrf"]):
        return "Fail", 400
    plans.delete_plan(request.form["plan_id"])
    return "Success", 200

@app.route("/train")
def prepare_training():
    if not user.is_logged_in():
        return redirect("/403")
    return render_template("preparetraining.html", plans=plans.get_users_plans())

@app.route("/train/<int:plan_id>/<int:position>")
def train_page(plan_id, position):
    if not user.is_logged_in():
        return redirect("/403")
    if training.is_over(plan_id, position):
        return redirect("/400")
    return render_template("train.html", data=training.get_content(plan_id, position), position=position, len=training.get_len(training.get_original_id(plan_id)), plan=plan_id, is_last=training.is_last(plan_id, position), recommendations=training.get_weight_and_reps_recommendation(plan_id, position))

@app.route("/nextmove", methods=["POST"])
def next_move():
    if not user.is_logged_in():
        return redirect("/403")
    if not user.check_csrf(request.form["csrf"]):
        return redirect("/400")
    rf = request.form
    nextpos = training.next_move(rf["plan_id"], rf["position"], rf["move_id"], rf["reps"], rf["weight"], rf["desc"])
    if training.is_over(rf["plan_id"], nextpos):
        return redirect("/")
    return redirect("/train/"+ str(rf["plan_id"]) +"/" + str(nextpos))
    
@app.route("/start", methods=["POST"])
def start_training():
    if not user.is_logged_in():
        return redirect("/403")
    if not user.check_csrf(request.form["csrf"]):
        return redirect("/400")
    new_training = training.initialize_new_training(request.form["plan_id"])
    return redirect("/train/"+ str(new_training) +"/1")

@app.route("/pasttrainings")
def get_trainings():
    if not user.is_logged_in():
        return redirect("/403")
    return render_template("oldtrainings.html", trainings=training.get_olds())

@app.route("/training/<int:tid>")
def get_training(tid):
    if not user.is_logged_in():
        return redirect("/403")
    return render_template("oldtraining.html", data=training.get_old_training(tid), info=plans.get_info(tid))

@app.route("/403")
def access_denied():
    return render_template("403.html")

@app.route("/400")
def bad_request():
    return render_template("400.html")