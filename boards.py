from db import db
import users

def get_boards():
    sql = "SELECT id, name FROM boards"
    result = db.session.execute(sql)
    return result.fetchall()

def get_boardname(id):
    sql = "SELECT name FROM boards WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_threads(id):
    sql = "SELECT * FROM threads t WHERE t.board_id =:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def create_thread(title, content, board_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (board_id, title, created_at, user_id) VALUES" \
          "(:board_id, :title, NOW(), :user_id) RETURNING id"
    result = db.session.execute(sql, {"board_id":board_id, "title":title, "user_id":user_id})
    thread_id = result.fetchone()[0]
    sql = "INSERT INTO comments (user_id, content, created_at, thread_id) VALUES" \
          "(:user_id, :content, NOW(), :thread_id)"
    db.session.execute(sql, {"user_id":user_id, "content":content, "thread_id":thread_id})
    db.session.commit()
    return True