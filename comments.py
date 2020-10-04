from db import db

def get_comment(id):
    sql = "SELECT * FROM comments WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def edit(content, id):
    sql = "UPDATE comments SET content=:content WHERE id=:id"
    db.session.execute(sql, {"content":content,"id":id})
    db.session.commit()
    return True

def remove(id):
    sql = "UPDATE comments SET visible=0 WHERE id=:id RETURNING thread_id"
    result = db.session.execute(sql, {"id":id})
    thread_id = result.fetchone()[0]
    db.session.commit()
    return thread_id

def search(query):
    #sql = "SELECT * FROM comments WHERE content LIKE :query"
    sql = "SELECT c.id, c.content, c.created_at, u.username FROM comments c " \
          "LEFT JOIN Users U ON c.user_id = u.id WHERE c.content LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()