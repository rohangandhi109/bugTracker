from app import db

class Project(db.Model):
    
    p_id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(20))
    p_desc = db.Column(db.String(100))
    p_start_date = db.Column(db.String)
    p_end_date = db.Column(db.String)
    
    def __init__(self, p_name, p_desc, p_start_date, p_end_date):
        self.p_name = p_name
        self.p_desc = p_desc
        self.p_start_date = p_start_date
        self.p_end_date = p_end_date
       
    def __repr__(self):
        return '<id {}>'.format(self.p_id)

    def format(self):
        return {
        'id': self.p_id,
        'name' : self.p_name,
        'desc' : self.p_desc,
        'start_date': self.p_start_date,
        'end_date' : self.p_end_date
        }

    def json_format(self):
        return{
            'p_id': self.p_id,
            'p_name': self.p_name
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        