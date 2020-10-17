from db import db
import users

def get_boards():
    sql = "SELECT id, boardname FROM boards WHERE secret=0"
    result = db.session.execute(sql)
    return result.fetchall()

def get_secret_boards():
    user_id = users.user_id()
    if users.user_role()==2:
        sql = "SELECT id, boardname FROM boards WHERE secret=1"
    else:
        sql = "SELECT b.id, b.boardname FROM boards b, SecretBoardUsers s WHERE secret=1 AND b.id=s.board_id AND s.user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_board(id):
    sql = "SELECT boardname, secret FROM boards WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_threads(id):
    sql = "SELECT t.id, t.title, u.username, t.created_at FROM threads t LEFT JOIN users u ON t.user_id=u.id WHERE t.board_id =:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def create_thread(title, content, board_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (board_id,user_id,title,opening_message,created_at) VALUES" \
          "(:board_id,:user_id,:title,:content,NOW())"
    db.session.execute(sql, {"board_id":board_id,"user_id":user_id,"title":title,"content":content})
    db.session.commit()
    return True

def create_board(boardname, secret):
    sql = "INSERT INTO boards (boardname, secret) VALUES (:boardname, :secret)"
    result = db.session.execute(sql, {"boardname":boardname, "secret":secret})
    db.session.commit()
    return True

def get_secret_board_users(board_id):
    sql = "SELECT u.id, u.username FROM users u, SecretBoardUsers s WHERE u.id = s.user_id AND s.board_id=:board_id"
    result = db.session.execute(sql, {"board_id":board_id})
    return result.fetchall()

def secret_board_access(board_id):
    user_id = users.user_id()
    if users.user_role()==2:
        sql = "SELECT board_id, user_id FROM SecretBoardUsers WHERE board_id=:board_id"
        return True
    else:
        sql = "SELECT board_id, user_id FROM SecretBoardUsers WHERE board_id=:board_id AND user_id=:user_id"
    result = db.session.execute(sql, {"board_id":board_id, "user_id":user_id})
    if result.fetchone() != None:
        return True
    return False

def invite_user(user_id, board_id):
    sql = "INSERT INTO SecretBoardUsers (user_id, board_id) VALUES (:user_id, :board_id)"
    db.session.execute(sql, {"user_id":user_id, "board_id":board_id})
    db.session.commit()
    return True

def remove_user(user_id, board_id):
    sql = "DELETE FROM SecretBoardUsers WHERE user_id=:user_id AND board_id=:board_id"
    db.session.execute(sql, {"user_id":user_id, "board_id":board_id})
    db.session.commit()
    return True