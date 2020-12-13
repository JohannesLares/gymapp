from db import db
import user

def create_new_plan(name, desc):
    if len(name) < 3:
        return "Nimi liian lyhyt"
    sql = "INSERT INTO plans (name, description, user_id) VALUES (:name,:desc,:user_id) RETURNING plan_id"  
    res = db.session.execute(sql, {"name": name, "desc": desc, "user_id": user.get_id()})
    db.session.commit()
    return_obj = res.fetchone()
    return return_obj["plan_id"]

def get_all():
    sql = "SELECT name, plan_id FROM plans WHERE user_id=:id AND training='f'"
    res = db.session.execute(sql, {"id": user.get_id()})
    return res.fetchall() 

def add_sets_to_new_plan(sets, amount, plan_id):
    sql = "SELECT user_id FROM plans WHERE plan_id=:pid"
    result = db.session.execute(sql, {"pid": plan_id})
    res = result.fetchone()
    if res["user_id"] != user.get_id():
        return False
    count = 1
    for i in range(amount):
        for x in range(int(sets[str(i)+"sets"])):
            if not sets[str(i)+"amount"]:
                continue
            sql = "INSERT INTO set (user_id, plan_id, move_id, place, reps) VALUES (:uid,:pid,:mid,:place,:reps)"
            db.session.execute(sql, {"uid": user.get_id(), "pid": plan_id, "mid": sets[str(i)+"move"], "place": count, "reps": sets[str(i)+"amount"]})
            count += 1
    db.session.commit()
    return True

def delete_set(set_id):
    sql = "SELECT plan_id FROM set WHERE set_id=:set_id AND user_id=:user_id"
    result = db.session.execute(sql, {"set_id": set_id, "user_id": user.get_id()})
    res = result.fetchone()
    if not res:
        return False
    pid = res["plan_id"]
    sql = "DELETE FROM set WHERE set_id=:set_id AND user_id=:user_id"
    res = db.session.execute(sql, {"set_id": set_id, "user_id": user.get_id()})
    db.session.commit()
    rearrange_on_delete(pid)
    return True

def get_one(plan_id):
    sql = "SELECT moves.name, set.place, set.reps, set.set_id FROM set INNER JOIN moves ON moves.move_id=set.move_id WHERE set.plan_id=:pid AND set.user_id=:uid ORDER BY set.place ASC"
    result = db.session.execute(sql, {"pid": plan_id, "uid": user.get_id()})
    res = result.fetchall()
    return res

def get_info(plan_id):
    sql = "SELECT name, user_id, description, plan_id FROM plans WHERE plan_id=:pid"
    result = db.session.execute(sql, {"pid": plan_id})
    res = result.fetchone()
    if res.user_id != user.get_id():
        return None
    return res

def get_users_plans():
    sql = "SELECT plan_id, name FROM plans WHERE user_id=:uid AND training='f'"
    result = db.session.execute(sql, {"uid": user.get_id()})
    res = result.fetchall()
    return res

def rearrange_on_delete(plan_id):
    sql = "SELECT set_id, place FROM set WHERE plan_id=:pid ORDER BY place"
    exres = db.session.execute(sql, {"pid": plan_id})
    rows = exres.fetchall()
    i = 1
    for row in rows:
        if row["place"] != i:
            db.session.execute("UPDATE set SET place=:ind WHERE set_id=:sid", {"ind": i, "sid": row["set_id"]})
        i += 1
    db.session.commit()
    return

def move_set(sid, new_place):
    res = db.session.execute("SELECT place, plan_id FROM set WHERE set_id=:set_id AND user_id=:uid", {"set_id": sid, "uid": user.get_id()})
    row = res.fetchone()
    if not row["place"]:
        return False
    plan = row["plan_id"]
    old_place = row["place"]
    db.session.execute("UPDATE set SET place=0 WHERE set_id=:sid AND plan_id=:pid", {"sid": sid, "pid": plan})
    if int(old_place) < int(new_place):
        for i in range(old_place, int(new_place)):
            db.session.execute("UPDATE set SET place=:new WHERE place=:old AND plan_id=:pid", {"new": i, "old": i+1, "pid": plan})
        db.session.execute("UPDATE set SET place=:new WHERE place=0 AND plan_id=:pid", {"new": new_place, "pid": plan})
        db.session.commit()
        return True
    else:
        for i in range(old_place, int(new_place)-1, -1):
            db.session.execute("UPDATE set SET place=:new WHERE place=:old AND plan_id=:pid", {"new": i+1, "old": i, "pid": plan})
        db.session.execute("UPDATE set SET place=:new WHERE place=0 AND plan_id=:pid", {"new": new_place, "pid": plan})
        db.session.commit()
        return True
    return False

def delete_plan(plan_id):
    db.session.execute("DELETE FROM set WHERE plan_id=:pid AND user_id=:uid", {"pid": plan_id, "uid": user.get_id()})
    db.session.execute("DELETE FROM plans WHERE plan_id=:pid AND user_id=:uid", {"pid": plan_id, "uid": user.get_id()})
    db.session.commit()
    return