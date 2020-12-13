from app import db

class Notification(db.Model):
    n_id = db.Column(db.Integer, primary_key=True)
    t_id = db.Column(db.Integer)
    users_id = db.Column(db.Integer)
    type = db.Column(db.String)
    
    def __init__(self, t_id, users_id, type):
        self.t_id = t_id
        self.users_id = users_id
        self.type = type
        
    def __repr__(self):
        return '<id {}>'.format(self.c_id)

    def format(self):
        return {
        'n_id' : self.n_id,
        't_id' : self.t_id,
        'users_id' : self.users_id,
        'type' : self.type,
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        