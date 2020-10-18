from db import db

def get_comment(id):
    sql = "SELECT user_id, content, thread_id, visible FROM comments WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def edit(content, id):
    try:
        sql = "UPDATE comments SET content=:content WHERE id=:id"
        db.session.execute(sql, {"content": content, "id": id})
        db.session.commit()
        return True
    except:
        return False

def remove(id):
    sql = "UPDATE comments SET visible=0 WHERE id=:id RETURNING thread_id"
    result = db.session.execute(sql, {"id": id})
    thread_id = result.fetchone()[0]
    db.session.commit()
    return thread_id

def search(query):
    # Haku toimii vain yleisiltä keskustelualueilta, jottei haun avulla pääsisi katsomaan salaisten alueiden tietoja.
    sql = "SELECT c.id, c.content, c.created_at, u.username, c.thread_id FROM comments c, boards b, threads t, users u " \
          "WHERE c.visible=1 AND c.user_id=u.id AND c.thread_id=t.id AND t.board_id=b.id AND b.secret=0 AND LOWER(c.content) LIKE LOWER(:query)"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    return result.fetchall()
