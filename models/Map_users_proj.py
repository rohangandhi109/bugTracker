from app import db

class Map_users_proj(db.Model):
    
    map_id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer)
    users_id = db.Column(db.Integer)
    users_role = db.Column(db.String)
    users_assign_date = db.Column(db.String)
    users_end_date = db.Column(db.String)


    def __init__(self, p_id, users_id, users_role, users_assign_date,users_end_date):
        self.p_id = p_id
        self.users_id = users_id
        self.users_role = users_role
        self.users_assign_date = users_assign_date
        self.users_end_date = users_end_date
       
    def __repr__(self):
        return '<id {}>'.format(self.map_id)

    def format(self):
        return {
        'id': self.map_id,
        'p_id' : self.p_id,
        'users_id' : self.users_id,
        'users_role': self.users_role,
        'users_assign_date' : self.users_assign_date,
        'users_end_date': self.users_end_date
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        