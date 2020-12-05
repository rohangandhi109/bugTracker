from app import db

class Map_emp_proj(db.Model):
    
    map_id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer)
    emp_id = db.Column(db.Integer)
    emp_role = db.Column(db.String)
    emp_assign_date = db.Column(db.String)
    emp_end_date = db.Column(db.String)


    def __init__(self, p_id, emp_id, emp_role, emp_assign_date,emp_end_date):
        self.p_id = p_id
        self.emp_id = emp_id
        self.emp_role = emp_role
        self.emp_assign_date = emp_assign_date
        self.emp_end_date = emp_end_date
       
    def __repr__(self):
        return '<id {}>'.format(self.map_id)

    def format(self):
        return {
        'id': self.map_id,
        'p_id' : self.p_id,
        'emp_id' : self.emp_id,
        'emp_role': self.emp_role,
        'emp_assign_date' : self.emp_assign_date,
        'emp_end_date': self.emp_end_date
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        