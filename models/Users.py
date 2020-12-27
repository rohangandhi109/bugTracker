from app import db
import sys

class Users(db.Model):
    users_id = db.Column(db.Integer, primary_key=True)
    users_email = db.Column(db.String)
    users_name =  db.Column(db.String)
    users_password = db.Column(db.String)
    users_role = db.Column(db.String)
    update_date = db.Column(db.String)
    
    def __init__(self, users_id,users_email, users_name, users_password, users_role, update_date):
        self.users_id = users_id
        self.users_email = users_email
        self.users_name = users_name
        self.users_password = users_password
        self.users_role = users_role
        self.update_date = update_date

    def __repr__(self):
        return '<id {}>'.format(self.users_id)

    def format(self):
        return {
        'id' : self.users_id,
        'email' : self.users_email,
        'name' : self.users_name,
        'password' : self.users_password,
        'role' : self.users_role,
        'update_date' : self.update_date

        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        