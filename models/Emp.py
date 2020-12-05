from app import db
import sys

class Emp(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_email = db.Column(db.String)
    emp_name =  db.Column(db.String)
    emp_password = db.Column(db.String)
    emp_role = db.Column(db.String)
    update_date = db.Column(db.String)
    
    def __init__(self, emp_email, emp_name, emp_password, emp_role, update_date):
        self.emp_email = emp_email
        self.emp_name = emp_name
        self.emp_password = emp_password
        self.emp_role = emp_role
        self.update_date = update_date

    def __repr__(self):
        return '<id {}>'.format(self.emp_id)

    def format(self):
        return {
            'id' : self.emp_id,
        'email' : self.emp_email,
        'name' : self.emp_name,
        'password' : self.emp_password,
        'role' : self.emp_role,
        'update_date' : self.update_date

        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        