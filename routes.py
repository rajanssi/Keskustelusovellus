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
        if len(username) < 3 :
            return render_template("register.html", errormessage="Käyttäjätunnuksen täytyy olla vähintään 3 merkkiä pitkä!")
        if len(password) < 6:
            return render_template("register.html", errormessage="Salasanan täytyy olla vähintään 6 merkkiä pitkä!")
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("register.html", errormessage="Rekisteröinti ei onnistunut")

@app.route("/board/<int:id>")
def board(id):
    board = boards.get_board(id)
    secretboardusers = boards.get_secret_board_users(id)
    threadlist = boards.get_threads(id)
    # Tarkastetaan, että käyttäjällä on pääsy salaisille keskustelualueille
    if board[1]==1 and boards.secret_board_access(id)==False:
        return redirect(url_for('error'))
    return render_template("board.html", id=id, boardname=board[0], threads=threadlist, secret=board[1], secretboardusers=secretboardusers)  

@app.route("/thread/<int:id>")
def thread(id):
    thread = threads.get_thread(id)
    board = boards.get_board(thread[2])
    comments = threads.get_comments(id)
    # Tarkastetaan, että käyttäjällä on pääsy salaisille keskustelualueille
    if board[1]==1 and boards.secret_board_access(thread[2])==False:
        return redirect(url_for('error'))
    return render_template("thread.html", id=id, title=thread[0], boardname=board[0], board_id=thread[2], comments=comments)

@app.route("/board/<int:id>/create-thread", methods=["GET", "POST"])
def create_thread(id):
    boardname = boards.get_board(id)[0]
    if not users.access_rights(users.user_id()):
        return redirect(url_for('error'))
    if request.method== "GET":
        return render_template("create-thread.html", id=id, boardname=boardname)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if len(title) < 2:
            return render_template("create-thread.html", id=id, boardname=boardname, errormessage="Otsikon täytyy olla vähintään 2 merkkiä pitkä.")
        if len(title) > 50:
            return render_template("create-thread.html", id=id, boardname=boardname, errormessage="Liian pitkä otsikko.")
        if len(content) < 2:
            return render_template("create-thread.html", id=id, boardname=boardname, errormessage="Viestin täytyy olla vähintään 2 merkkiä pitkä.")
        if len(content) > 1000:
            return render_template("create-thread.html", id=id, boardname=boardname, errormessage="Viesti on liian pitkä")
        thread_id = boards.create_thread(title, content, id)
        if thread_id:
            return redirect(url_for('thread', id=thread_id))
        else:
            return render_template("create-thread.html", id=id, boardname=boardname, errormessage="Keskustelun luonti ei onnistunut")

@app.route("/thread/<int:id>/reply", methods=["POST"])
def reply(id):
    if not users.access_rights(users.user_id()):
        return redirect(url_for('error'))
    content = request.form["content"]
    if len(content) < 3:
        return redirect(url_for('thread', id=id))
    if threads.reply(content, id):
        return redirect(url_for('thread', id=id))
    else:
        return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_comment(id):
    comment = comments.get_comment(id)
    if comment == None or comment[3]==0:
        return redirect(url_for('error'))
    thread_id = comment[2]
    thread = threads.get_thread(thread_id)
    board_id = thread[2]
    board = boards.get_board(board_id)
    if not users.access_rights(comment[0]):
        return redirect(url_for('error'))
    if request.method == "GET":
        return render_template("edit-comment.html", id=id, comment=comment[1], board_id=board_id, boardname=board[0], 
                                thread_id=thread_id,  thread_title=thread[0])
    if request.method == "POST":
        content = request.form["content"]
        if len(content) < 2:
            return render_template("edit-comment.html", id=id, comment=comment[1], board_id=board_id, boardname=board[0], 
                                    thread_id=thread_id,  thread_title=thread[0], errormessage="Viestin täytyy olla vähintään 2 merkkiä pitkä.")
        if len(content) > 1000:
            return render_template("edit-comment.html", id=id, comment=comment[1], board_id=board_id, boardname=board[0], 
                                    thread_id=thread_id,  thread_title=thread[0], errormessage="Viesti on liian pitkä!")
        if comments.edit(content, id):
            return redirect(url_for('thread', id=thread_id))
        else:
            return render_template("edit-comment.html", id=id, comment=comment[1], board_id=board_id, boardname=board[0], 
                                    thread_id=thread_id,  thread_title=thread[0], errormessage="Viestin muokkaus ei onnistunut")

@app.route("/remove/<int:id>")
def remove_comment(id):
    user_id = comments.get_comment(id)[0]
    if not users.access_rights(user_id):
        return redirect(url_for('error'))
    thread_id = comments.remove(id)
    return redirect(url_for('thread', id=thread_id))

@app.route("/search")
def search():
    query = request.args["query"]
    commentList = comments.search(query)
    return render_template("search.html", commentList=commentList, query=query)

@app.route("/create-board", methods=["GET", "POST"])
def create_board():
    if users.user_role() != 2:
        return redirect(url_for('error'))
    if request.method == "GET":
        return render_template("create-board.html")
    if request.method == "POST":
        boardname = request.form["boardname"]
        if request.form.get("secret") == None:
            secret = 0
        else: 
            secret = 1
        if boards.create_board(boardname, secret):
            return redirect("/")
        else:
            return render_template("create-board.html")

@app.route("/board/<int:id>/invite", methods=["GET", "POST"])
def invite(id):
    board_users = boards.get_secret_board_users(id)
    board = boards.get_board(id)
    userlist = users.get_users()
    if users.user_role() != 2:
        return redirect(url_for('error'))
    if request.method == "GET":
        return render_template("invite.html", id=id, boardname=board[0], board_users=board_users, userlist=userlist)
    if request.method == "POST":
        user_id = request.form["users"]
        if int(user_id)==0:
            return render_template("invite.html", id=id, boardname=board[0], board_users=board_users, userlist=userlist, errormessage="Valitse käyttäjä!")
        # Tarkastetaan, onko käyttäjä jo alueella
        user_invited = False
        for row in board_users:
                for elem in row:
                    if int(user_id) == elem:
                        user_invited = True
        if request.form["submit"] == 'remove':
            if not user_invited:
                return render_template("invite.html", id=id, boardname=board[0], board_users=board_users, userlist=userlist, errormessage="Käyttäjä ei ole alueella!")
            if boards.remove_user(user_id, id):
                board_users = boards.get_secret_board_users(id)
                return render_template("invite.html", id=id, boardname=board[0], board_users=board_users, userlist=userlist)
        elif request.form["submit"] == 'add':
            if user_invited:
                return render_template("invite.html", id=id, boardname=board[0], board_users=board_users, userlist=userlist, errormessage="Käyttäjä on jo lisätty!")
            if boards.invite_user(user_id, id):
                board_users = boards.get_secret_board_users(id)
                return render_template("invite.html", id=id, boardname=board[0], board_users=board_users, userlist=userlist)

@app.route("/error")
def error():
    return render_template("error.html")