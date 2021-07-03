from . import db #Get the Database from within the directory
from flask_login import UserMixin
from sqlalchemy.sql import func

class Product(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(200), unique=True)
    prod_price = db.Column(db.String(100))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #Takes ID as the primary key or unique identifier
    email = db.Column(db.String(150), unique=True) # Defined email as a unique value
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    logs = db.relationship('Log')