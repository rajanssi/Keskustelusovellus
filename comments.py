from db import db

def get_comment(id):
    sql = "SELECT * FROM comments WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def edit(content, id):
    sql = "UPDATE comments SET content=:content WHERE id=:id"
    db.session.execute(sql, {"content":content,"id":id})
    db.session.commit()
    return True

def remove(id):
    sql = "DELETE FROM comments WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True