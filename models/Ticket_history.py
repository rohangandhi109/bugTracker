from app import db

class Ticket_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_id = db.Column(db.Integer)
    users_id = db.Column(db.Integer)
    t_status =  db.Column(db.String)
    t_update_date = db.Column(db.String)
    priority = db.Column(db.String)
    
    def __init__(self, id, t_id, users_id, t_status, t_update_date, priority):
        self.id = id
        self.t_id = t_id
        self.users_id = users_id
        self.t_status = t_status
        self.t_update_date = t_update_date
        self.priority = priority

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def format(self):
        return {
        'id' : self.t_id,
        'users_id' : self.users_id,
        'status' : self.t_status,
        'priority' : self.priority,
        'update_date' : self.t_update_date
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        