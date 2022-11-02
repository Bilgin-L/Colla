from extensions import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)


class CategoryModel(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    color = db.Column(db.String(100), nullable=False, unique=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # User id will be the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # If you want to get all the categories of a user, you can write it through categories
    user = db.relationship("UserModel", backref="categories")
