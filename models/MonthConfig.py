from app import db

class MonthConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mth_id = db.Column(db.Integer)
    mth_name = db.Column(db.String)
    mth_year = db.Column(db.Integer)

    def __init__(self, mth_name, mth_year):
        self.mth_name = mth_name
        self.mth_year = mth_year


    def format(self):
        return {
        'month': self.month,
        'p_id' : self.p_id,
        'cnt' : self.cnt,
        'name': self.name,
        }
    
    def pie_fromat(self):
        return{
            'priority' : self.priority,
            'cnt': self.cnt
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

