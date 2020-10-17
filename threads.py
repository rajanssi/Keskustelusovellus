from db import db
import users

def get_thread(id):
    sql = "SELECT t.title, t.opening_message, b.boardname, b.id FROM threads T LEFT JOIN boards b " \
        "ON t.board_id = b.id WHERE t.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_threadtitle(id):
    sql = "SELECT title FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_openingMessage(id):
    sql = "SELECT opening_message FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_comments(id):
    sql = "SELECT c.id, c.content, c.created_at, c.user_id, u.username, c.visible FROM comments c " \
          "LEFT JOIN Users U ON c.user_id = u.id WHERE c.thread_id=:id ORDER BY c.id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def reply(content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO comments (user_id, content, created_at, thread_id) VALUES" \
          "(:user_id, :content, NOW(), :thread_id)"
    db.session.execute(sql, {"user_id":user_id, "content":content, "thread_id":thread_id})
    db.session.commit()
    return True

def reply_count(id):
    sql = "SELECT count(*) FROM comments WHERE thread_id:id AND visible=1"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]