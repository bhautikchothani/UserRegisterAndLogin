from app import db,bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import column,Integer,String


class Credentials(db.Model,UserMixin):
    # __tablename__="credentials"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(200), nullable=False)
    phone_number =  db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(120))
        
    def set_password(self, password):  # class user_data in user_password using 
        self.password = bcrypt.generate_password_hash(password).decode("utf-8") #       

    def check_password(self, password): # class user_data in user_password using check a password
        return bcrypt.check_password_hash(self.password,password)
    
    # this function make for the profile update 
    def update_profile(self, username, email, mobile,photo):
        self.username = username
        self.email = email
        self.mobile = mobile
        self.photo = photo
        db.session.commit()