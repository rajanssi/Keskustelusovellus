from db import db
import os
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


def get_users():
    sql = "SELECT id, username FROM users WHERE role = 1"
    result = db.session.execute(sql)
    return result.fetchall()


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["username"] = username
            session["user_role"] = user[2]
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False


def user_id():
    return session.get("user_id", 0)


def user_role():
    return session.get("user_role", 0)


def get_username(id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()[0]


def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]


def access_rights(id):
    if user_id() == 0:
        return False
    if user_role() == 2:
        return True
    if user_id() == id:
        return True
    return False
