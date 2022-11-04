from flask import g, redirect, url_for
from functools import wraps
from models import CategoryModel, TodoModel
from extensions import db


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
