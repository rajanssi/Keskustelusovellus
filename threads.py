from db import db
import users

def get_threadtitle(id):
    sql = "SELECT title FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_comments(id):
    sql = "SELECT * FROM comments c WHERE c.thread_id =:id"
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