from flask import Flask
from flask import render_template , url_for , redirect , request , jsonify , session , Response
from flask_session import Session 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
app.config['SECRET_KEY']='ar12@gtmnB'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///main.db'
db=SQLAlchemy(app)

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),default='')
    student_id= db.Column(db.Integer(),unique=True,nullable=False)
    password_hash =db.Column(db.String(128),nullable=False)
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    def __init__(self,student_id,name):
        self.student_id=student_id
        self.name=name

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    genre_id = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, heading, image , genre_id):
        self.heading = heading
        self.image = image
        self.genre_id=genre_id

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)

class BookGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))


class SessionModel(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    data = db.Column(db.PickleType())
    expiry = db.Column(db.DateTime)