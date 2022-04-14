from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Enum, ForeignKeyConstraint, func
db = SQLAlchemy()

#I used these websties to help me with all of the foreign keys/relationships:
# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

#This is to represent the many to many relationship between users and friend (must be made before each entity table)
friends = db.Table('friend',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
)

#This is the begining of each entity in our database
class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(45), nullable=False)
    f_name = db.Column(db.String(45), nullable=False)
    l_name = db.Column(db.Integer, nullable=False)
    comments = db.relationship('Comments', backref='users', lazy=True)
    posts = db.relationship('Post', backref='users', lazy=True)
    contact = db.relationship('Contact', backref='users', lazy=True)
    friends = db.relationship('friend', secondary=friends, lazy='subquery', backref=db.backref('friend', lazy=True))

class Friend(db.Model):
    __tablename__ = 'friend'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    friend_id = db.Column(db.Interger, primary_key=True, nullable=False)
    pending = db.Column(db.Boolean, nullable=False)
    #Need to add foreign key for user_id and friend_id to both reference user_id

class Comments(db.Model):
    __tablename__ = 'comments'
    com_thread_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comment = db.Column(db.String(255))
    posts = db.relationship('Post', backref='comments', lazy=True)


#I used this website to help me create this enum:
#https://stackoverflow.com/questions/2676133/best-way-to-do-enum-in-sqlalchemy
#This is for the post_label that we allow users to select when creating a post
class post_enum(Enum.Enum):
    campus = 'campus'
    sports = 'sports'
    stuorg = 'student org'
    norm = 'norm'
    alums = 'alums'
    meme = 'meme'

class Post(db.Model):
    __tablename__ = 'post'    
    post_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(45), db.ForeignKey('users.user_name'), nullable=False)
    post_label = db.Column(Enum(post_enum))
    post_cap = db.Column(db.String(255), nullable=True)
    com_thread_id = db.Column(db.Integer, db.ForeignKey('comments.com_thread_id'), nullable=False)

#I used this webstie to help with the date attribute
# https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
class Contact(db.Model):
    __tablename__ = 'contact'
    contact_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    email = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(255), nullable=True)


