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


class TodoModel(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_code = db.Column(db.String(100), nullable=False, unique=False)
    module_name = db.Column(db.String(100), nullable=False, unique=False)
    assessment_name = db.Column(db.String(100), nullable=False, unique=False)
    due_date = db.Column(db.DateTime, nullable=False, unique=False)
    description = db.Column(db.String(500), nullable=True, unique=False)
    # status - 0: not started, 1: completed
    status = db.Column(db.Integer, nullable=False, unique=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # email_inform - 0: not inform, 1: inform
    email_inform = db.Column(db.Integer, nullable=False, unique=False)
    # status_email - 0: not send, 1: send
    status_email = db.Column(db.Integer, nullable=False, unique=False)
    # status_notification - 0: not send, 1: send
    status_notification = db.Column(db.Integer, nullable=False, unique=False)
    # important - 0: not important, 1: important
    important = db.Column(db.Integer, nullable=False, unique=False)
    # trash - 0: not in trash, 1: in trash
    trash = db.Column(db.Integer, nullable=False, unique=False)
    # User id will be the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # Category id will be the foreign key
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    # If you want to get all the todos of a user, you can write it through todos
    user = db.relationship("UserModel", backref="todos")
    # If you want to get all the todos of a category, you can write it through todos
    category = db.relationship("CategoryModel", backref="todos")
