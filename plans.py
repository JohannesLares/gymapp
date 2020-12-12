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
    sql = "SELECT * FROM plans WHERE user_id=:id"
    res = db.session.execute(sql, {"id": user.get_id()})
    return res.fetchall() 

def add_sets_to_new_plan(sets, amount, plan_id):
    sql = "SELECT user_id FROM plans WHERE plan_id=:pid"
    result = db.session.execute(sql, {"pid": plan_id})
    res = result.fetchone()
    if res["user_id"] != user.get_id():
        return False
    count = 0
    for i in range(amount):
        for x in range(int(sets[str(i)+"sets"])):
            sql = "INSERT INTO set (user_id, plan_id, move_id, place, reps) VALUES (:uid,:pid,:mid,:place,:reps)"
            db.session.execute(sql, {"uid": user.get_id(), "pid": plan_id, "mid": sets[str(i)+"move"], "place": count, "reps": sets[str(i)+"amount"]})
            count += 1
    db.session.commit()
    return True

def delete_set(set_id):
    sql = "DELETE FROM set WHERE set_id=:set_id AND user_id=:user_id"
    res = db.session.execute(sql, {"set_id": set_id, "user_id": user.get_id()})
    db.session.commit()
    return True

def get_one(plan_id):
    sql = "SELECT moves.name, set.place, set.reps, set.set_id FROM set INNER JOIN moves ON moves.move_id=set.move_id WHERE set.plan_id=:pid AND set.user_id=:uid ORDER BY set.place ASC"
    result = db.session.execute(sql, {"pid": plan_id, "uid": user.get_id()})
    res = result.fetchall()
    return(res)

def get_info(plan_id):
    sql = "SELECT name, user_id, description FROM plans WHERE plan_id=:pid"
    result = db.session.execute(sql, {"pid": plan_id})
    res = result.fetchone()
    if res.user_id != user.get_id():
        return None
    return res