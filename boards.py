from db import db
import users

def get_boards():
    sql = "SELECT id, boardname FROM boards"
    result = db.session.execute(sql)
    return result.fetchall()

def get_secret_boards():
    user_id = users.user_id()
    sql = "SELECT p.id, p.boardname FROM privateBoards p, privateBoardsUsers b WHERE p.id=b.board_id AND b.user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_boardname(id):
    sql = "SELECT boardname FROM boards WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_threads(id):
    sql = "SELECT t.id, t.title FROM threads t WHERE t.board_id =:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def create_thread(title, content, board_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (board_id,user_id,title,opening_message,created_at) VALUES" \
          "(:board_id,:user_id,:title,:content,NOW())"
    result = db.session.execute(sql, {"board_id":board_id,"user_id":user_id,"title":title,"content":content})
    db.session.commit()
    return True