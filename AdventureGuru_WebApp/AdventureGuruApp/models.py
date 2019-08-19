from AdventureGuruApp import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash= db.Column(db.String(128))

    posts = db.relationship('CNN', backref='CNN_model', lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"

class Destination(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(140),nullable=False)
    location =  db.Column(db.String(64),nullable=False)
    type =  db.Column(db.String(64),nullable=False)
    cost = db.Column(db.Integer,nullable=False)
    length = db.Column(db.Integer,nullable = False)
    text = db.Column(db.Text,nullable=False)
    imageFile = db.Column(db.String(64),nullable=False)

    def __init__(self,title ,location ,type , cost, length, text ,imageFile):
        self.title = title
        self.location = location
        self.type = type
        self.cost = cost
        self.length = length
        self.text = text
        self.imageFile = imageFile

    def __repr__(self):
        return f"Title: {self.title} -- Location: {self.location} -- Type: {self.type}"

class CNN(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- Title: {self.title}"
