from AdventureGuruApp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class Demo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_file = db.Column(db.String(140),nullable=False)
    iterations = db.Column(db.Integer,nullable=False)
    trainLoss = db.Column(db.Float,nullable=False)
    trainAcc = db.Column(db.Float,nullable=False)

    def __init__(self,model_file,iterations,trainLoss,trainAcc):
        self.model_file = model_file
        self.iterations = iterations
        self.trainLoss = trainLoss
        self.trainAcc = trainAcc

    def __repr__(self):
        return f"ID: {self.id} -- Model: {self.model_file} -- Iterations: {self.iterations} -- Loss: {self.trainLoss}-- Acc: {self.trainAcc} "

    def __json__(self):
        return {"ID": self.id, "Model": {self.model_file}, "Iterations": {self.iterations}, "Loss": {self.trainLoss}, "Acc": {self.trainAcc}}

association_table = db.Table('association',
    db.Column('dest_id',db.Integer,db.ForeignKey('dest.id')),
    db.Column('type_id',db.Integer,db.ForeignKey('type.id')),
    db.Column('time_id',db.Integer,db.ForeignKey('time.id')),
    db.Column('age_id',db.Integer,db.ForeignKey('age.id'))
    )

class Destination(db.Model):
    __tablename__ = 'dest'

    #ID
    id = db.Column(db.Integer, primary_key=True)
    #Basic Attributes
    title = db.Column(db.String(64),nullable=False)
    location =  db.Column(db.String(64),nullable=False)
    country = db.Column(db.String(64),nullable=False)
    imageFilename = db.Column(db.String(64),nullable=False)
    #Characteristics
    category = db.Column(db.String(64),nullable=False)
    cost = db.Column(db.Integer) #Range 1 to 5
    accessibility = db.Column(db.Integer) #Range 1 to 3 - 1:easy, 2:moderate 3:hard
    types =  db.relationship('Type',secondary=association_table,backref='destinations',lazy=True) #List of types
    times = db.relationship('Time',secondary=association_table,backref='destinations',lazy=True) #List of times
    ages =  db.relationship('Age',secondary=association_table,backref='destinations',lazy=True) #List of ages

    def __init__(self, title ,location ,country,category, imagefilename):
        self.title = title
        self.location = location
        self.country = country
        self.category = category
        self.imageFilename = imagefilename

    def json(self):
        ageList = ""
        timeList = ""
        typeList = ""

        for feature in self.types:
            if typeList:
                typeList+=","
            typeList+=feature.title

        for feature in self.ages:
            if ageList:
                ageList+=","
            ageList+=feature.title

        for feature in self.times:
            if timeList:
                timeList+=","
            timeList+=feature.title

        return {'title': self.title,
                'location':self.location,
                'country':self.country,
                'imageFilename':self.imageFilename,
                'category': self.category,
                'cost': self.cost,
                'accessibility': self.accessibility,
                'types': typeList,
                'times': timeList,
                'ages': ageList
                }

    def __repr__(self):
        return f"Title: {self.title} -- Location: {self.location} -- Country: {self.country} -- Filename: {self.imageFilename}"

class Type(db.Model):
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(64),nullable=False)

    def __init__(self,title):
        self.title = title

    def json(self):
        return {'title': self.title}

    def __repr__(self):
        return f"Title: {self.title}"

class Time(db.Model):
    __tablename__ = 'time'

    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(64),nullable=False)

    def __init__(self,title):
        self.title = title

    def json(self):
        return {'title': self.title}

    def __repr__(self):
        return f"Title: {self.title}"


class Age(db.Model):
    __tablename__ = 'age'

    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(64),nullable=False)

    def __init__(self,title):
        self.title = title

    def json(self):
        return {'title': self.title}

    def __repr__(self):
        return f"Title: {self.title}"

'''
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
'''
