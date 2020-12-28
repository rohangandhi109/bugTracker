from app import db

class Comment(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    t_id = db.Column(db.Integer)
    users_id = db.Column(db.Integer)
    date = db.Column(db.String)
    comment = db.Column(db.String)
    
    def __init__(self, c_id, t_id, users_id, t_update_date, comment):
        self.c_id = c_id
        self.t_id = t_id
        self.users_id = users_id
        self.date = t_update_date
        self.comment = comment

    def __repr__(self):
        return '<id {}>'.format(self.c_id)

    def format(self):
        return {
        't_id' : self.t_id,
        'users_id' : self.users_id,
        'comment' : self.comment,
        'date' : self.date
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        