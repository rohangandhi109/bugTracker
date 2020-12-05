from app import db
import sys

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String)
    user_name =  db.Column(db.String)
    user_password = db.Column(db.String)
    user_role = db.Column(db.String)
    update_date = db.Column(db.String)
    
    def __init__(self, user_email, user_name, user_password, user_role, update_date):
        self.user_email = user_email
        self.user_name = user_name
        self.user_password = user_password
        self.user_role = user_role
        self.update_date = update_date

    def __repr__(self):
        return '<id {}>'.format(self.user_id)

    def format(self):
        return {
        'id' : self.user_id,
        'email' : self.user_email,
        'name' : self.user_name,
        'password' : self.user_password,
        'role' : self.user_role,
        'update_date' : self.update_date

        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        