from app import app
from db import db
from flask import render_template, redirect, request

@app.route("/")
def index():
    sql = "SELECT id, title FROM subforums"
    result = db.session.execute(sql)
    subforums = result.fetchall()
    return render_template("index.html", subforums=subforums)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/subforum/<int:id>")
def subforum(id):
    sql = "SELECT title FROM subforums WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    forumname = result.fetchone()[0]
    sql  = "SELECT * FROM threads t WHERE t.subforum_id =:subforum_id"
    result = db.session.execute(sql, {"subforum_id":id})
    threads = result.fetchall()
    
    return render_template("subforum.html", forumname=forumname, threads=threads)  
    
@app.route("/newthread")
def newthread():
    return render_template("register.html")

