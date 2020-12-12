from db import db
import user

def initialize_new_training(plan_id):
    res = db.session.execute("SELECT name, description FROM plans WHERE plan_id=:pid AND user_id=:uid AND training='f'", {"pid": plan_id, "uid": user.get_id()})
    plan = res.fetchone()
    if not plan:
        return None
    psql = "INSERT INTO plans (name, description, user_id, training, copyof) VALUES (:n, :d, :uid, 't', :cid) RETURNING plan_id"
    new_plan = db.session.execute(psql, {"n": plan["name"], "d": plan["description"], "uid": user.get_id(), "cid": plan_id})
    db.session.commit()
    res = new_plan.fetchone()
    return res[0]

def get_content(pid, pos):
    res = db.session.execute("SELECT copyof FROM plans WHERE plan_id=:pid AND user_id=:uid AND training='t'", {"pid": pid, "uid": user.get_id()})
    result = res.fetchone()
    if not result:
        return "error"
    copyof = result[0]
    set_sql = "SELECT * FROM set INNER JOIN moves ON set.move_id = moves.move_id WHERE set.plan_id=:pid AND set.user_id=:uid AND set.place=:pos"
    res = db.session.execute(set_sql, {"pid": copyof, "uid": user.get_id(), "pos": pos})
    result = res.fetchone()
    if not result:
        return "error"
    print(result)
    return result

def next_move(pid, pos, move_id, reps, weight, desc):
    sql = "INSERT INTO set (plan_id, move_id, user_id, place, weight, time, reps, description) VALUES (:pid, :mid, :uid, :place, :weight, NOW(), :reps, :description)"
    db.session.execute(sql, {"pid": pid, "mid": move_id, "uid": user.get_id(), "place": pos, "weight": weight, "reps": reps, "description": desc})
    db.session.commit()
    return int(pos)+1

def is_last(pid, pos):
    sql = "SELECT copyof FROM plans WHERE plan_id=:pid AND user_id=:uid"
    res = db.session.execute(sql, {"pid": pid, "uid": user.get_id()})
    result = res.fetchone()
    return pos == get_len(result[0])

def get_len(pid):
    sql = "SELECT place FROM set WHERE plan_id=:pid AND user_id=:uid"
    res = db.session.execute(sql, {"pid": pid, "uid": user.get_id()})
    result = res.fetchall()
    return len(result)

def get_olds():
    sql = "SELECT * FROM plans WHERE user_id=:uid AND training='t'"
    res = db.session.execute(sql, {"uid": user.get_id()})
    result=res.fetchall()
    return result