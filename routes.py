from app import app
import boards, users, threads, comments
from flask import render_template, redirect, request, url_for


@app.route("/")
def index():
    boardlist = boards.get_boards()
    secretboardlist = boards.get_secret_boards()
    return render_template("index.html", boards=boardlist, secretboards=secretboardlist)

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
            return render_template("login.html", errormessage="Väärä tunnus tai salasana")

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
        if len(username) < 1 :
            return render_template("register.html", errormessage="Käyttäjätunnuksen täytyy olla vähintään 2 merkkiä pitkä.")
        if len(password) < 5:
            return render_template("register.html", errormessage="Salasanan täytyy olla vähintään 6 merkkiä pitkä.")
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("register.html", errormessage="Rekisteröinti ei onnistunut")

@app.route("/board/<int:id>")
def board(id):
    boardname = boards.get_boardname(id)
    threads = boards.get_threads(id)
    return render_template("board.html", id=id, boardname=boardname, threads=threads)  

@app.route("/thread/<int:id>")
def thread(id):
    title = threads.get_threadtitle(id)
    openingmessage = threads.get_openingMessage(id)
    comments = threads.get_comments(id)
    return render_template("thread.html", id=id, openingmessage=openingmessage, title=title, comments=comments)

@app.route("/board/<int:id>/create-thread", methods=["GET", "POST"])
def create_thread(id):
    if request.method== "GET":
        return render_template("create-thread.html", id=id)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if len(title) < 1:
            return render_template("create-thread.html", id=id, errormessage="Otsikon täytyy olla vähintään 2 merkkiä pitkä.")
        if len(title) > 50:
            return render_template("create-thread.html", id=id, errormessage="Liian pitkä otsikko.")
        if len(content) < 1:
            return render_template("create-thread.html", id=id, errormessage="Viestin täytyy olla vähintään 2 merkkiä pitkä.")
        if len(content) > 1000:
            return render_template("create-thread.html", id=id, errormessage="Viesti on liian pitkä")
        if boards.create_thread(title, content, id):
            return redirect(url_for('board', id=id))
        else:
            return render_template("create-thread.html", errormessage="Keskustelun luonti ei onnistunut")

@app.route("/thread/<int:id>/reply", methods=["POST"])
def reply(id):
    content = request.form["content"]
    if len(content) < 1:
        return render_template("error.html", errormessage="Viestin täytyy olla vähintään 2 merkkiä pitkä.")
    if threads.reply(content, id):
        return redirect(url_for('thread', id=id))
    else:
        return render_template("error.html", errormessage="Vastauksen lähetys ei onnistunut")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_comment(id):
    comment = comments.get_comment(id)
    thread_id = comment[2]
    if users.user_id() != comment[1]:
        return redirect("/")
    if request.method == "GET":
        return render_template("edit-comment.html", id=id)
    if request.method == "POST":
        content = request.form["content"]
        if len(content) < 1:
            return render_template("edit-comment.html", errormessage="Viestin täytyy olla vähintään 2 merkkiä pitkä.")
        if comments.edit(content, id):
            return redirect(url_for('thread', id=thread_id))
        else:
            return render_template("edit-comment.html", errormessage="Viestin muokkaus ei onnistunut")

@app.route("/remove/<int:id>")
def remove_comment(id):
    thread_id = comments.remove(id)
    return redirect(url_for('thread', id=thread_id))

@app.route("/search-results")
def searchresults():
    query = request.args["query"]
    commentList = comments.search(query)
    return render_template("search-results.html", commentList=commentList, query=query)