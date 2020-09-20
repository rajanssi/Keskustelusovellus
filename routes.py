from app import app
from db import db
import boards, users, threads, comments
from flask import render_template, redirect, request, url_for


@app.route("/")
def index():
    list = boards.get_boards()
    return render_template("index.html", boards=list)

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

@app.route("/board/<int:id>")
def board(id):
    boardname = boards.get_boardname(id)
    threads = boards.get_threads(id)
    return render_template("board.html", id=id, boardname=boardname, threads=threads)  

@app.route("/thread/<int:id>")
def thread(id):
    title = threads.get_threadtitle(id)
    comments = threads.get_comments(id)
    return render_template("thread.html", id=id, title=title, comments=comments)

@app.route("/board/<int:id>/create-thread", methods=["get", "post"])
def create_thread(id):
    if request.method== "GET":
        return render_template("create-thread.html", id=id)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if boards.create_thread(title, content, id):
            return redirect(url_for('board', id=id))
        else:
            return render_template("error.html", message="Keskustelun luonti ei onnistunut")

@app.route("/thread/<int:id>/reply", methods=["post"])
def reply(id):
    content = request.form["content"]
    if threads.reply(content, id):
        return redirect(url_for('thread', id=id))
    else:
        return render_template("error.html", message="Vastauksen lähetys ei onnistunut")

@app.route("/edit/<int:id>", methods=["get", "post"])
def edit_comment(id):
    if request.method == "GET":
        return render_template("edit-comment.html", id=id)
    if request.method == "POST":
        content = request.form["content"]
        if comments.edit(content, id):
            return redirect("/")
        else:
            return render_template("error.html", message="Viestin muokkaus ei onnistunut")

@app.route("/remove/<int:id>")
def remove_comment(id):
    comments.remove(id)
    return redirect("/")