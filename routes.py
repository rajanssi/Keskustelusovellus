from app import app
from db import db
import boards, users
from flask import render_template, redirect, request

message2 = 'Testi'

@app.route("/")
def index():
    sql = "SELECT id, boardname FROM boards"
    result = db.session.execute(sql)
    boards = result.fetchall()
    return render_template("index.html", message2=message2, boards=boards)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")
    return render_template("login.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/boards/<int:id>")
def boards(id):
    sql = "SELECT boardname FROM boards WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    boardname = result.fetchone()[0]
    sql  = "SELECT * FROM threads t WHERE t.board_id =:board_id"
    result = db.session.execute(sql, {"board_id":id})
    threads = result.fetchall()
    return render_template("boards.html", boardname=boardname, threads=threads)  
    
@app.route("/newthread")
def newthread():
    return render_template("register.html")

