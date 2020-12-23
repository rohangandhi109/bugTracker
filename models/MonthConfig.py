from app import db

class MonthConfig(db.Model):
    mth_id = db.Column(db.Integer, primary_key=True)
    mth_name = db.Column(db.String)

    def format(self):
        return {
        'month': self.month,
        'p_id' : self.p_id,
        'cnt' : self.cnt
        }
