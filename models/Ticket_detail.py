from app import db

class Ticket_detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_id = db.Column(db.Integer)
    emp_id = db.Column(db.Integer)
    t_status =  db.Column(db.String)
    t_update_date = db.Column(db.String)
    comment = db.Column(db.String)
    
    def __init__(self, t_id, emp_id, t_status, t_update_date, comment):
        self.t_id = t_id
        self.emp_id = emp_id
        self.t_status = t_status
        self.t_update_date = t_update_date
        self.comment = comment

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def format(self):
        return {
        'id' : self.t_id,
        'emp_id' : self.emp_id,
        'status' : self.t_status,
        'comment' : self.comment,
        'update_date' : self.t_update_date
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        