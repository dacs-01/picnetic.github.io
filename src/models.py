import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Enum, ForeignKeyConstraint, func
#longtext found from this link https://stackoverflow.com/questions/61684135/how-to-represent-longtext-in-sqlalchemy
from sqlalchemy.dialects.mysql import LONGTEXT
db = SQLAlchemy()


#I used these websties to help me with all of the foreign keys/relationships:
# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
#https://michaelcho.me/article/using-python-enums-in-sqlalchemy-models

#This is to represent the many to many relationship between users and friend (must be made before each entity table)
#friends = db.Table('friends',
#    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
#    db.Column('friend_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
#)

#This is the begining of each entity in our database

class Enum(db.TypeDecorator):
     #passes in a python enum and stores the value in the db. Used this because before we were just getting post_enum.name instead of just name. 
    impl = db.String
    #
    def __init__(self, enumtype, *args, **kwargs):
            super(Enum, self).__init__(*args, **kwargs)
            self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        #check if it is an instance of the enum table and if it is then just return the value
        if isinstance(value, int):
            return value

        return value.value



class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    passed = db.Column(LONGTEXT, nullable=False)
    f_name = db.Column(db.String(255), nullable= True)
    l_name = db.Column(db.Integer, nullable= True)
    comments = db.relationship('Comments', backref='users', lazy=True)
    posts = db.relationship('Post', backref='users', lazy=True)
    contact = db.relationship('Contact', backref='users', lazy=True)
    #friends = db.relationship('friend', secondary=friends, lazy='subquery', backref=db.backref('friend', lazy=True))

class Friend(db.Model):
    __tablename__ = 'friend'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    friend_id = db.Column(db.Integer, primary_key=True, nullable=False)
    pending = db.Column(db.Boolean, nullable=False)
    #Need to add foreign key for user_id and friend_id to both reference user_id

class Comments(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comment = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)

#I used this website to help me create this enum:
#https://stackoverflow.com/questions/2676133/best-way-to-do-enum-in-sqlalchemy
#This is for the post_label that we allow users to select when creating a post
class post_enum(enum.Enum):
    campus = 'campus'
    sports = 'sports'
    studentOrg = 'student org'
    norm = 'norm'
    alums = 'alums'
    meme = 'meme'

class Post(db.Model):
    __tablename__ = 'post'    
    post_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(45), db.ForeignKey('users.user_name'), nullable=False)
    post_label = db.Column(db.String(255), nullable=True)
    post_cap = db.Column(db.String(255), nullable=True)
    post_picture = db.Column(db.String(255), nullable=False)
    #picture_file_name = db.Column(db.Text, nullable=False)

#I used this webstie to help with the date attribute
# https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
class Contact(db.Model):
    __tablename__ = 'contact'
    contact_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    email = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(255), nullable=True)
