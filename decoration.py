from flask import g, redirect, url_for, flash
from functools import wraps
from models import CategoryModel, TodoModel
from extensions import db, mail
import datetime
from flask_mail import Message


def login_required(func):
    # 这个@wrap装饰器一定不要忘记写了
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("views.login"))
    return wrapper


def check_category(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get a category id which name is 'Default' to the current user
        category = CategoryModel.query.filter_by(name="Default", user_id=g.user.id).first()
        # If the category is not exist, create a new category
        if not category:
            category = CategoryModel(name="Default", color="blue", user_id=g.user.id)
            db.session.add(category)
            db.session.commit()
        # Traverse all todos of the current user
        todos = TodoModel.query.filter_by(user_id=g.user.id).all()
        # if there is a todos without category, then redirect add a category called 'Default' to this to
        for todo in todos:
            if todo.category is None:
                todo.category_id = category.id
                db.session.commit()
        return func(*args, **kwargs)
    return wrapper


def email_inform(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Traverse all todos of the current user
        todos = TodoModel.query.filter_by(user_id=g.user.id).all()
        # If the time of todos is less than 24 hours and 'email_inform' is 1 and 'status_email' is 0, then send an email
        for todo in todos:
            if todo.due_date - datetime.datetime.now() < datetime.timedelta(hours=24) and todo.email_inform == 1 and todo.status_email == 0:
                # Send an email
                msg = Message(
                    subject="[Colla] - !! Reminder !!",
                    recipients=[g.user.email],
                    body="Hi, " + g.user.username + ":\n\n" +
                         "You have a todo ' " + todo.assessment_name + " ' which is due in 24 hours.\n\n" +
                         "Best regards,\n" +
                         "Colla Team"
                )
                mail.send(msg)
                todo.status_email = 1
                db.session.commit()
        return func(*args, **kwargs)
    return wrapper
