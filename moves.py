from db import db
import user

def get_all():
    sql = "SELECT * FROM moves WHERE public OR user_id=:id"
    result = db.session.execute(sql, {"id": user.get_id()})
    moves = []
    for row in result:
        d = dict(row)
        if d["user_id"] == user.get_id():
            d["own"] = True
        moves.append(d)
    return moves

def get_one(move_id):
    sql = "SELECT * FROM moves WHERE move_id=:move_id AND (public OR user_id=:user_id)"
    result = db.session.execute(sql, {"move_id": move_id, "user_id": user.get_id()})
    res = result.fetchone()
    move = dict(res)
    print(move)
    if move["user_id"] == user.get_id():
        move["own"] = True
    return move

def create_new(name, desc, public):
    message = ""
    if not user.is_admin() and public != "f":
        public = "f"
        message = "Vaihdettu julkisesta privaksi. "
    if len(name) < 3:
        return "Nimi liian lyhyt"
    sql = "INSERT INTO moves (name, description, public, user_id) VALUES (:name,:desc,:public,:user_id)"  
    db.session.execute(sql, {"name": name, "desc": desc, "public": public, "user_id": user.get_id()})
    db.session.commit()
    return message + "Tallennettu"

def edit_one(move_id, name, description, public): 
    message = ""
    if not user.is_admin() and public != "f":
        public = "f"
        message = "Vaihdettu julkisesta privaksi. "
    sql = "UPDATE moves SET name=:name, description=:description, public=:public WHERE move_id=:move_id AND user_id=:user_id"
    db.session.execute(sql, {"name": name, "description": description, "public": public, "move_id": move_id, "user_id": user.get_id()})
    db.session.commit()
    return True